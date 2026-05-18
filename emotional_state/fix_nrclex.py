"""
NRC EmoLex 修復腳本
===================
修復 NRCLex 載入失敗的問題，嘗試多種方式取得 NRC 情緒詞典。

使用方式:
    pip install nrclex
    python fix_nrclex.py

會產出: nrc_emolex_by_emotion.csv
"""

import os
import json
import csv
import sys
from collections import defaultdict


def try_load_nrclex():
    """嘗試多種方式載入 NRC EmoLex。"""

    # ── 方法 1: 直接用 NRCLex 物件測試 ──
    print("[方法 1] 用 NRCLex 物件逐詞查詢...")
    try:
        from nrclex import NRCLex

        # 先找到 nrclex 的安裝路徑
        import nrclex as nrc_module
        pkg_dir = os.path.dirname(nrc_module.__file__)
        print(f"    NRCLex 安裝路徑: {pkg_dir}")
        print(f"    該目錄下的檔案:")
        for f in os.listdir(pkg_dir):
            print(f"      {f}")

        # 嘗試各種可能的檔名
        possible_files = [
            os.path.join(pkg_dir, 'nrc_en.json'),
            os.path.join(pkg_dir, 'nrc_en.csv'),
            os.path.join(pkg_dir, 'nrc_emotion_lexicon.json'),
            os.path.join(pkg_dir, 'data', 'nrc_en.json'),
            os.path.join(pkg_dir, 'lexicon', 'nrc_en.json'),
        ]

        for fpath in possible_files:
            if os.path.exists(fpath):
                print(f"    ✅ 找到檔案: {fpath}")
                if fpath.endswith('.json'):
                    return load_from_json(fpath)
                elif fpath.endswith('.csv'):
                    return load_from_csv_file(fpath)

        # 如果都找不到，搜尋整個套件目錄
        print("    正在搜尋整個套件目錄...")
        for root, dirs, files in os.walk(pkg_dir):
            for fname in files:
                if 'nrc' in fname.lower() and (fname.endswith('.json') or fname.endswith('.csv') or fname.endswith('.txt')):
                    full_path = os.path.join(root, fname)
                    print(f"    找到: {full_path}")

    except ImportError:
        print("    ⚠️  NRCLex 未安裝")

    # ── 方法 2: 用 textdata R package 的下載方式（Python 版）──
    print("\n[方法 2] 直接從 NRC 官網結構下載...")
    try:
        import requests
        # NRC EmoLex 的公開 GitHub 備份
        urls = [
            "https://raw.githubusercontent.com/sebastianruder/emotion_proposition_store/master/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt",
            "https://raw.githubusercontent.com/dinbav/LeXmo/master/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt",
        ]

        for url in urls:
            print(f"    嘗試下載: {url[:80]}...")
            try:
                resp = requests.get(url, timeout=30)
                if resp.status_code == 200:
                    return parse_nrc_txt(resp.text)
            except Exception as e:
                print(f"    ❌ {e}")
                continue

    except ImportError:
        print("    ⚠️  requests 未安裝")

    # ── 方法 3: 用 NRCLex 的 API 逐詞測試來反向建構詞典 ──
    print("\n[方法 3] 透過 NRCLex API 反向載入...")
    try:
        from nrclex import NRCLex

        # 用一個已知的情緒詞測試
        test = NRCLex("happy sad angry fearful")
        if test.affect_frequencies:
            print(f"    NRCLex 功能正常！")
            print(f"    測試結果: {test.affect_frequencies}")

            # 嘗試存取內部詞典
            if hasattr(test, 'lexicon') and test.lexicon:
                return convert_nrclex_lexicon(test.lexicon)

            # 嘗試存取類別屬性
            for attr_name in dir(test):
                if 'lex' in attr_name.lower() or 'dict' in attr_name.lower():
                    attr = getattr(test, attr_name)
                    if isinstance(attr, dict) and len(attr) > 100:
                        print(f"    找到內部詞典: {attr_name} ({len(attr)} entries)")

        print("    ℹ️  NRCLex 可以用，但無法直接匯出完整詞典。")
        print("       建議手動下載 NRC EmoLex:")
        print("       https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm")

    except ImportError:
        pass

    return None


def load_from_json(filepath):
    """從 JSON 檔載入。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = defaultdict(set)
    if isinstance(data, dict):
        for word, emotions in data.items():
            if isinstance(emotions, list):
                for emo in emotions:
                    results[emo].add(word)
            elif isinstance(emotions, dict):
                for emo, score in emotions.items():
                    if score and (score == 1 or score == '1' or score is True):
                        results[emo].add(word)

    print(f"    ✅ 載入成功！")
    return dict(results)


def load_from_csv_file(filepath):
    """從 CSV 檔載入。"""
    results = defaultdict(set)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3:
                word, emotion, flag = row[0], row[1], row[2]
                if flag.strip() == '1':
                    results[emotion.strip()].add(word.strip())

    print(f"    ✅ 載入成功！")
    return dict(results)


def parse_nrc_txt(text):
    """解析 NRC EmoLex 的 tab-separated 格式。"""
    results = defaultdict(set)
    for line in text.strip().split('\n'):
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            word, emotion, flag = parts[0], parts[1], parts[2]
            if flag.strip() == '1':
                results[emotion.strip()].add(word.strip())

    if results:
        print(f"    ✅ 下載並解析成功！")
    return dict(results) if results else None


def convert_nrclex_lexicon(lexicon):
    """將 NRCLex 的內部格式轉為我們的格式。"""
    results = defaultdict(set)
    for word, emotions in lexicon.items():
        if isinstance(emotions, list):
            for emo in emotions:
                results[emo].add(word)
        elif isinstance(emotions, dict):
            for emo, score in emotions.items():
                if score:
                    results[emo].add(word)
    return dict(results)


def save_results(results):
    """儲存結果。"""
    if not results:
        print("\n❌ 無法取得 NRC EmoLex 資料。")
        print("   請手動下載:")
        print("   https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm")
        return

    # 統計
    all_words = set()
    print("\n📊 NRC EmoLex 統計:")
    print("-" * 40)
    for cat in sorted(results.keys()):
        words = results[cat]
        all_words.update(words)
        print(f"   {cat:20s} {len(words):>6,}")
    print("-" * 40)
    print(f"   {'TOTAL UNIQUE':20s} {len(all_words):>6,}")

    # 儲存 CSV
    rows = []
    for category, words in sorted(results.items()):
        for word in sorted(words):
            rows.append({"emotion": category, "word": word})

    output_file = "nrc_emolex_by_emotion.csv"
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["emotion", "word"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ 儲存到: {output_file}")
    print(f"   共 {len(rows)} 筆 (word, emotion) 組合")
    print(f"   共 {len(all_words)} 個不重複的詞")

    # 也存一份純關鍵字
    kw_file = "nrc_emolex_keywords.txt"
    with open(kw_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(sorted(all_words)))
    print(f"   關鍵字清單: {kw_file}")


def main():
    print("=" * 50)
    print("NRC EmoLex 載入修復工具")
    print("=" * 50)

    results = try_load_nrclex()
    save_results(results)

    print("\n💡 這份 CSV 可以和之前的 emotion_keywords_by_category.csv 合併使用")


if __name__ == "__main__":
    main()
