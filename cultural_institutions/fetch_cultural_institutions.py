"""
Cultural Institutions Keyword Collector
=======================================
從 Wikidata 批次下載全球文化機構名稱，自動分頁避免 timeout。

使用方式:
    pip install requests pandas
    python fetch_cultural_institutions.py

輸出:
    cultural_institutions_all.csv  — 合併所有類別的結果
    cultural_institutions/         — 每個類別的個別 CSV
"""

import requests
import pandas as pd
import time
import os
import sys

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

HEADERS = {
    "User-Agent": "CulturalInstitutionsBot/1.0 (Research project; contact: your_email@example.com)",
    "Accept": "application/json"
}

# =====================================================================
# 定義所有要查詢的文化機構類別
# 每個類別單獨查詢，避免 VALUES 造成的效能問題
# =====================================================================
INSTITUTION_TYPES = {
    # --- Museums ---
    "museum":                  "Q33506",
    "art_museum":              "Q207694",
    "history_museum":          "Q2772772",
    "science_museum":          "Q2301048",
    "natural_history_museum":  "Q2677461",
    "archaeological_museum":   "Q4989906",
    "military_museum":         "Q1970365",
    "children_museum":         "Q16735822",
    "ethnographic_museum":     "Q15206070",
    "maritime_museum":         "Q1473674",
    "open_air_museum":         "Q575727",
    "aviation_museum":         "Q3658083",
    "technology_museum":       "Q1955659",
    "memorial_museum":         "Q2772759",

    # --- Performing Arts ---
    "opera_house":             "Q153562",
    "theater_building":        "Q24354",
    "concert_hall":            "Q1060829",
    "performing_arts_center":  "Q17088587",

    # --- Libraries & Archives ---
    "national_library":        "Q856234",
    "public_library":          "Q28564",
    "archive":                 "Q166118",
    "national_archive":        "Q2860008",

    # --- Galleries & Cultural Centers ---
    "art_gallery":             "Q1007870",
    "cultural_center":         "Q18674739",

    # --- Nature & Science ---
    "botanical_garden":        "Q167346",
    "zoo":                     "Q43229",
    "aquarium":                "Q2281788",
    "planetarium":             "Q41176",
    "science_center":          "Q1292588",

    # --- Festivals ---
    "film_festival":           "Q220505",
    "music_festival":          "Q2153354",
    "arts_festival":           "Q868557",

    # --- Heritage ---
    "world_heritage_site":     "Q9259",
}


def build_query(qid: str, limit: int = 5000, offset: int = 0) -> str:
    """
    建立簡單的 SPARQL query，一次只查一個類別。
    不使用 P279*（子類別遞迴），不使用 ORDER BY，以求最快速度。
    """
    return f"""
SELECT ?item ?itemLabel ?itemAltLabel ?countryLabel WHERE {{
  ?item wdt:P31 wd:{qid} .
  OPTIONAL {{ ?item wdt:P17 ?country . }}
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "en,zh,zh-tw,zh-cn,fr,de,es,it,ja,ko,ar,ru,pt,hi,th,vi,id,tr,pl,nl,sv,he,fa,uk" .
  }}
}}
LIMIT {limit}
OFFSET {offset}
"""


def query_wikidata(sparql: str, max_retries: int = 3) -> list:
    """送出 SPARQL query，自動重試。"""
    for attempt in range(max_retries):
        try:
            resp = requests.get(
                WIKIDATA_ENDPOINT,
                params={"query": sparql, "format": "json"},
                headers=HEADERS,
                timeout=90
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("results", {}).get("bindings", [])
            elif resp.status_code == 429:
                # Rate limited — 等久一點再試
                wait = 30 * (attempt + 1)
                print(f"    ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif resp.status_code in (500, 502, 503, 504):
                wait = 15 * (attempt + 1)
                print(f"    ⚠️  Server error {resp.status_code}, retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"    ❌ HTTP {resp.status_code}: {resp.text[:200]}")
                return []
        except requests.exceptions.Timeout:
            wait = 20 * (attempt + 1)
            print(f"    ⏳ Timeout, retrying in {wait}s (attempt {attempt+1}/{max_retries})...")
            time.sleep(wait)
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Request error: {e}")
            return []
    return []


def parse_results(bindings: list) -> list[dict]:
    """將 Wikidata JSON 結果轉為 dict list。"""
    rows = []
    for b in bindings:
        rows.append({
            "wikidata_id":   b.get("item", {}).get("value", "").split("/")[-1],
            "name_en":       b.get("itemLabel", {}).get("value", ""),
            "alt_names":     b.get("itemAltLabel", {}).get("value", ""),
            "country":       b.get("countryLabel", {}).get("value", ""),
        })
    return rows


def fetch_all_for_type(type_name: str, qid: str, page_size: int = 5000) -> pd.DataFrame:
    """
    對某個類別進行分頁查詢，直到沒有更多結果。
    """
    all_rows = []
    offset = 0

    while True:
        sparql = build_query(qid, limit=page_size, offset=offset)
        bindings = query_wikidata(sparql)

        if not bindings:
            break

        rows = parse_results(bindings)
        all_rows.extend(rows)
        print(f"    📦 Got {len(rows)} items (total: {len(all_rows)})")

        if len(bindings) < page_size:
            break  # 最後一頁

        offset += page_size
        time.sleep(2)  # 禮貌等待，避免被 rate limit

    df = pd.DataFrame(all_rows)
    if not df.empty:
        df["type"] = type_name
        df = df.drop_duplicates(subset=["wikidata_id"])
    return df


def extract_keywords(df: pd.DataFrame) -> list[str]:
    """
    從結果中提取所有不重複的名稱/關鍵字。
    包含英文名稱和所有 alt_names（在地語言）。
    """
    keywords = set()

    for _, row in df.iterrows():
        # English name
        name = str(row.get("name_en", "")).strip()
        if name and name != row.get("wikidata_id", ""):
            keywords.add(name)

        # Alt names (comma-separated)
        alts = str(row.get("alt_names", "")).strip()
        if alts:
            for alt in alts.split(","):
                alt = alt.strip()
                if alt and alt != name:
                    keywords.add(alt)

    return sorted(keywords)


def main():
    output_dir = "cultural_institutions"
    os.makedirs(output_dir, exist_ok=True)

    all_dfs = []
    total_types = len(INSTITUTION_TYPES)

    print("=" * 60)
    print("Cultural Institutions Keyword Collector")
    print(f"Querying {total_types} institution types from Wikidata...")
    print("=" * 60)

    for i, (type_name, qid) in enumerate(INSTITUTION_TYPES.items(), 1):
        print(f"\n[{i}/{total_types}] 🏛️  {type_name} ({qid})")

        # 檢查是否已有快取
        cache_path = os.path.join(output_dir, f"{type_name}.csv")
        if os.path.exists(cache_path):
            print(f"    ✅ Already cached, loading from {cache_path}")
            df = pd.read_csv(cache_path)
        else:
            df = fetch_all_for_type(type_name, qid)
            if not df.empty:
                df.to_csv(cache_path, index=False, encoding="utf-8-sig")
                print(f"    💾 Saved to {cache_path}")
            else:
                print(f"    ⚠️  No results")
            time.sleep(3)  # 每個類別之間等待

        if not df.empty:
            all_dfs.append(df)

    # 合併所有結果
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined = combined.drop_duplicates(subset=["wikidata_id"])

        # 儲存完整 CSV
        combined.to_csv("cultural_institutions_all.csv", index=False, encoding="utf-8-sig")
        print(f"\n✅ Combined CSV saved: cultural_institutions_all.csv")
        print(f"   Total unique institutions: {len(combined)}")

        # 提取關鍵字清單
        keywords = extract_keywords(combined)
        with open("cultural_institutions_keywords.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(keywords))
        print(f"   Total unique keywords: {len(keywords)}")
        print(f"   Keywords saved to: cultural_institutions_keywords.txt")

        # 按類別統計
        print("\n📊 Summary by type:")
        print("-" * 40)
        for type_name in INSTITUTION_TYPES:
            count = len(combined[combined["type"] == type_name])
            if count > 0:
                print(f"   {type_name:30s} {count:>6,}")
        print("-" * 40)
        print(f"   {'TOTAL':30s} {len(combined):>6,}")
    else:
        print("\n❌ No data collected.")

    print("\nDone! 🎉")


if __name__ == "__main__":
    main()
