"""
Emotional States Keyword Collector
====================================
下載並合併多個 NLP 情緒詞典，產出分類好的情緒關鍵字清單。

使用方式:
    pip install requests pandas nrclex afinn nltk
    python fetch_emotion_keywords.py

輸出:
    emotion_keywords_by_category.csv  — 按情緒類別分組的完整清單
    emotion_keywords_all.txt          — 所有不重複的情緒詞（一行一個）
    emotion_lexicons_guide.txt        — 各詞典來源說明
"""

import os
import csv
import json
import requests
import pandas as pd
from collections import defaultdict

# =============================================================================
# PART 0: 輸出資源指南
# =============================================================================

GUIDE_TEXT = """
=================================================================
EMOTIONAL STATE KEYWORDS — 資源指南
=================================================================

你的 keyword collector 的情緒詞可以從以下來源取得。
本腳本會自動處理標示 [AUTO] 的來源，標示 [MANUAL] 的需要手動下載。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [AUTO] NRC EmoLex（最推薦）
   - 14,182 個英文詞，標註 8 種情緒 + 正負面
   - 情緒類別: anger, anticipation, disgust, fear, joy, sadness, surprise, trust
   - 有 100+ 語言翻譯版
   - 免費用於研究
   - 下載: https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm
   - GitHub 備份: https://github.com/sebastianruder/emotion_proposition_store/tree/master/NRC-Emotion-Lexicon-v0.92

2. [AUTO] NRC VAD Lexicon
   - 20,000+ 個英文詞
   - 三個維度: Valence (正負面), Arousal (激動程度), Dominance (掌控感)
   - 下載: https://saifmohammad.com/WebPages/nrc-vad.html

3. [AUTO] NRC Emotion Intensity Lexicon
   - 5,814 個英文詞
   - 4 種情緒強度分數: anger, fear, sadness, joy
   - 下載: https://saifmohammad.com/WebPages/AffectIntensity.htm

4. [AUTO] AFINN-111
   - 2,477 個英文詞/片語
   - Valence 分數 -5 到 +5
   - 包含社群媒體用語和俚語
   - pip install afinn

5. [AUTO] VADER Lexicon
   - 7,500+ 個英文詞
   - 專為社群媒體設計，包含 emoji、俚語、縮寫
   - Valence 分數 -4 到 +4
   - pip install vaderSentiment 或
   - https://github.com/cjhutto/vaderSentiment

6. [AUTO] NRCLex Python Package
   - 整合了 NRC EmoLex，可直接用 Python 查詢
   - pip install nrclex

7. [MANUAL] LIWC (Linguistic Inquiry and Word Count)
   - 學術界最常用的文字分析工具
   - 需要購買授權 (~$200/年)
   - 情緒類別非常細緻（包含 positive emotion, negative emotion,
     anxiety, anger, sadness 等子類別）
   - https://www.liwc.app/

8. [MANUAL] ANEW (Affective Norms for English Words)
   - 1,034 個英文詞
   - Valence, Arousal, Dominance 三維度（1-9 分）
   - 需向作者申請: Bradley & Lang (1999)
   - 心理學實驗標準

9. [AUTO] SentiWordNet
   - 基於 WordNet，每個 synset 有正面/負面/客觀分數
   - NLTK 可直接存取
   - https://github.com/aesuli/SentiWordNet

10. [MANUAL] WorryWords (2024 新！)
    - 44,000+ 個英文詞的焦慮關聯分數
    - Saif Mohammad, EMNLP 2024
    - https://saifmohammad.com/WebPages/lexicons.html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

建議策略:
  Step 1: 用本腳本自動合併 NRC EmoLex + AFINN + VADER（免費、自動化）
  Step 2: 手動下載 NRC VAD（20,000 詞的 valence score，你提到的）
  Step 3: 如果學校有 LIWC 授權，用它補充更細的分類
  Step 4: 用 Plutchik's Wheel of Emotions 作為分類框架整理

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Plutchik's 8 基本情緒 (+ 組合情緒):

  基本情緒          相反情緒        組合情緒
  ─────────────────────────────────────────────
  Joy        ←→    Sadness        Joy + Trust = Love
  Trust      ←→    Disgust        Trust + Fear = Submission
  Fear       ←→    Anger          Fear + Surprise = Awe
  Surprise   ←→    Anticipation   Surprise + Sadness = Disapproval
  Sadness    ←→    Joy            Sadness + Disgust = Remorse
  Disgust    ←→    Trust          Disgust + Anger = Contempt
  Anger      ←→    Fear           Anger + Anticipation = Aggressiveness
  Anticipation ←→  Surprise       Anticipation + Joy = Optimism

=================================================================
"""


# =============================================================================
# PART 1: 用 NRCLex 自動取得 NRC EmoLex 分類
# =============================================================================

def get_nrclex_words():
    """從 NRCLex package 取得情緒詞典。"""
    print("\n[1/4] Loading NRC EmoLex via NRCLex package...")
    try:
        from nrclex import NRCLex
        # NRCLex 內建了完整的 NRC 詞典
        # 我們需要直接存取它的內部詞典
        import nrclex
        lexicon_path = os.path.join(os.path.dirname(nrclex.__file__), 'nrc_en.json')

        if os.path.exists(lexicon_path):
            with open(lexicon_path, 'r', encoding='utf-8') as f:
                lexicon = json.load(f)

            results = defaultdict(set)
            for word, emotions in lexicon.items():
                for emotion in emotions:
                    results[emotion].add(word)

            total = len(set(w for words in results.values() for w in words))
            print(f"    ✅ Loaded {total} words across {len(results)} emotion categories")
            for cat, words in sorted(results.items()):
                print(f"       {cat}: {len(words)} words")
            return dict(results)
        else:
            print("    ⚠️  NRCLex lexicon file not found at expected path")
            return {}

    except ImportError:
        print("    ⚠️  NRCLex not installed. Run: pip install nrclex")
        print("       Falling back to manual NRC loading...")
        return get_nrc_from_github()


def get_nrc_from_github():
    """從 GitHub 備份下載 NRC EmoLex。"""
    print("    Downloading NRC EmoLex from GitHub...")
    url = "https://raw.githubusercontent.com/sebastianruder/emotion_proposition_store/master/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            results = defaultdict(set)
            for line in resp.text.strip().split('\n'):
                if line.startswith('#') or not line.strip():
                    continue
                parts = line.strip().split('\t')
                if len(parts) == 3:
                    word, emotion, flag = parts
                    if flag == '1':
                        results[emotion].add(word)
            total = len(set(w for words in results.values() for w in words))
            print(f"    ✅ Downloaded {total} words")
            return dict(results)
        else:
            print(f"    ❌ HTTP {resp.status_code}")
            return {}
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return {}


# =============================================================================
# PART 2: AFINN valence words
# =============================================================================

def get_afinn_words():
    """從 AFINN package 取得 valence 詞典。"""
    print("\n[2/4] Loading AFINN lexicon...")
    try:
        from afinn import Afinn
        afinn = Afinn()
        # AFINN 的內部詞典
        results = {
            "afinn_very_negative": set(),   # -5 to -3
            "afinn_negative": set(),         # -2 to -1
            "afinn_positive": set(),         # +1 to +2
            "afinn_very_positive": set(),    # +3 to +5
        }

        # 存取 AFINN 的內部字典
        for word, score in afinn._dict.items():
            if score <= -3:
                results["afinn_very_negative"].add(word)
            elif score < 0:
                results["afinn_negative"].add(word)
            elif score >= 3:
                results["afinn_very_positive"].add(word)
            elif score > 0:
                results["afinn_positive"].add(word)

        total = sum(len(v) for v in results.values())
        print(f"    ✅ Loaded {total} words")
        for cat, words in sorted(results.items()):
            print(f"       {cat}: {len(words)} words")
        return results

    except ImportError:
        print("    ⚠️  AFINN not installed. Run: pip install afinn")
        return {}


# =============================================================================
# PART 3: VADER lexicon
# =============================================================================

def get_vader_words():
    """從 VADER 取得情緒詞典（含 emoji 和社群媒體用語）。"""
    print("\n[3/4] Loading VADER lexicon...")
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()

        results = {
            "vader_very_negative": set(),
            "vader_negative": set(),
            "vader_positive": set(),
            "vader_very_positive": set(),
        }

        for word, score in analyzer.lexicon.items():
            if score <= -2.0:
                results["vader_very_negative"].add(word)
            elif score < 0:
                results["vader_negative"].add(word)
            elif score >= 2.0:
                results["vader_very_positive"].add(word)
            elif score > 0:
                results["vader_positive"].add(word)

        total = sum(len(v) for v in results.values())
        print(f"    ✅ Loaded {total} words/tokens")
        for cat, words in sorted(results.items()):
            print(f"       {cat}: {len(words)} words")
        return results

    except ImportError:
        print("    ⚠️  VADER not installed. Run: pip install vaderSentiment")
        return {}


# =============================================================================
# PART 4: 額外的手動情緒詞清單（心理學 / ESL 教學常用）
# =============================================================================

def get_manual_emotion_words():
    """
    心理學和英語教學中常見的情緒詞彙分類。
    這些是 NLP 詞典可能遺漏的日常用語和片語。
    """
    print("\n[4/4] Adding manually curated emotion vocabulary...")

    results = {
        # --- Plutchik's 8 基本情緒的擴展詞彙 ---
        "joy_extended": {
            "happy", "joyful", "elated", "blissful", "ecstatic", "delighted",
            "cheerful", "jubilant", "euphoric", "overjoyed", "thrilled",
            "content", "pleased", "satisfied", "grateful", "thankful",
            "merry", "gleeful", "radiant", "beaming", "grinning",
            "laughing", "amused", "entertained", "playful", "lighthearted",
            "carefree", "upbeat", "optimistic", "hopeful", "encouraged",
            "inspired", "motivated", "energized", "exhilarated", "alive",
            "blessed", "fortunate", "lucky", "wonderful", "fantastic",
            "amazing", "awesome", "great", "terrific", "superb",
            "on cloud nine", "over the moon", "walking on air",
            "on top of the world", "in high spirits", "tickled pink",
        },

        "sadness_extended": {
            "sad", "unhappy", "sorrowful", "mournful", "grieving", "heartbroken",
            "devastated", "crushed", "dejected", "despondent", "depressed",
            "melancholy", "gloomy", "somber", "dismal", "bleak",
            "miserable", "wretched", "woeful", "pitiful", "pathetic",
            "lonely", "isolated", "abandoned", "forsaken", "neglected",
            "homesick", "nostalgic", "longing", "yearning", "pining",
            "disappointed", "let down", "disillusioned", "hopeless", "despairing",
            "helpless", "powerless", "vulnerable", "fragile", "broken",
            "tearful", "weeping", "sobbing", "crying", "whimpering",
            "down in the dumps", "feeling blue", "heavy-hearted",
            "brokenhearted", "crestfallen", "downhearted",
        },

        "anger_extended": {
            "angry", "furious", "enraged", "livid", "irate", "outraged",
            "incensed", "infuriated", "seething", "fuming", "boiling",
            "irritated", "annoyed", "aggravated", "exasperated", "frustrated",
            "resentful", "bitter", "hostile", "antagonistic", "belligerent",
            "indignant", "offended", "insulted", "provoked", "agitated",
            "heated", "fired up", "worked up", "wound up", "riled up",
            "vengeful", "vindictive", "spiteful", "wrathful", "murderous",
            "seeing red", "hot under the collar", "blowing a fuse",
            "at the end of one's rope", "fit to be tied",
        },

        "fear_extended": {
            "afraid", "scared", "frightened", "terrified", "petrified",
            "horrified", "panic-stricken", "alarmed", "startled", "shocked",
            "anxious", "worried", "nervous", "uneasy", "apprehensive",
            "dreadful", "dreading", "fearing", "trembling", "shaking",
            "intimidated", "threatened", "vulnerable", "insecure", "paranoid",
            "phobic", "claustrophobic", "agoraphobic", "panicked", "hysterical",
            "spooked", "creeped out", "freaked out", "scared stiff",
            "frozen with fear", "shaking in one's boots",
            "on edge", "walking on eggshells", "butterflies in stomach",
        },

        "surprise_extended": {
            "surprised", "astonished", "amazed", "stunned", "astounded",
            "flabbergasted", "dumbfounded", "speechless", "thunderstruck",
            "bewildered", "baffled", "perplexed", "confounded", "mystified",
            "startled", "jolted", "taken aback", "caught off guard",
            "blindsided", "floored", "gobsmacked", "shell-shocked",
            "incredulous", "disbelieving", "wide-eyed", "jaw-dropping",
            "mind-blowing", "mind-boggling", "eye-opening", "unexpected",
        },

        "disgust_extended": {
            "disgusted", "revolted", "repulsed", "nauseated", "sickened",
            "appalled", "horrified", "abhorrent", "loathing", "detesting",
            "repelled", "grossed out", "turned off", "put off",
            "contemptuous", "scornful", "disdainful", "sneering",
            "squeamish", "queasy", "sick to one's stomach",
        },

        "trust_extended": {
            "trusting", "confident", "assured", "secure", "safe",
            "comfortable", "relaxed", "at ease", "calm", "peaceful",
            "faithful", "loyal", "devoted", "committed", "reliable",
            "dependable", "trustworthy", "honest", "sincere", "genuine",
            "believing", "convinced", "certain", "sure", "positive",
        },

        "anticipation_extended": {
            "anticipating", "expecting", "awaiting", "eager", "excited",
            "enthusiastic", "impatient", "restless", "itching", "yearning",
            "longing", "craving", "desiring", "wanting", "wishing",
            "hoping", "optimistic", "looking forward", "can't wait",
            "on the edge of one's seat", "counting down",
            "suspenseful", "tense", "anxious", "apprehensive", "nervous",
        },

        # --- 額外心理狀態（不在 Plutchik 8 種中）---
        "love_affection": {
            "love", "loving", "adoring", "cherishing", "devoted",
            "passionate", "romantic", "infatuated", "smitten", "besotted",
            "affectionate", "tender", "caring", "compassionate", "empathetic",
            "warm", "fond", "attached", "bonded", "connected",
            "head over heels", "madly in love", "crazy about",
            "falling for", "swept off feet",
        },

        "pride_confidence": {
            "proud", "accomplished", "triumphant", "victorious", "successful",
            "confident", "self-assured", "bold", "courageous", "brave",
            "empowered", "strong", "capable", "competent", "worthy",
            "dignified", "honored", "respected", "admired", "esteemed",
        },

        "shame_guilt": {
            "ashamed", "embarrassed", "humiliated", "mortified", "sheepish",
            "guilty", "remorseful", "regretful", "sorry", "apologetic",
            "disgraced", "dishonored", "degraded", "unworthy", "inadequate",
            "self-conscious", "exposed", "judged", "stigmatized",
        },

        "confusion_uncertainty": {
            "confused", "puzzled", "perplexed", "baffled", "bewildered",
            "disoriented", "lost", "uncertain", "unsure", "doubtful",
            "hesitant", "indecisive", "ambivalent", "torn", "conflicted",
            "overwhelmed", "flustered", "rattled", "discombobulated",
        },

        "boredom_apathy": {
            "bored", "uninterested", "indifferent", "apathetic", "listless",
            "lethargic", "sluggish", "unmotivated", "uninspired", "dull",
            "monotonous", "tedious", "weary", "fatigued", "exhausted",
            "burnt out", "drained", "numb", "detached", "disconnected",
        },

        "jealousy_envy": {
            "jealous", "envious", "covetous", "possessive", "resentful",
            "begrudging", "green with envy", "green-eyed",
        },

        "loneliness_isolation": {
            "lonely", "alone", "isolated", "solitary", "desolate",
            "abandoned", "forsaken", "rejected", "excluded", "ostracized",
            "alienated", "disconnected", "estranged", "cut off",
            "homesick", "missing someone",
        },

        # --- 身心狀態（跟健康詞有交叉，但偏情緒面）---
        "stress_anxiety": {
            "stressed", "anxious", "tense", "strained", "pressured",
            "overwhelmed", "overloaded", "swamped", "stretched thin",
            "burned out", "frazzled", "frantic", "panicky",
            "worried sick", "stressed out", "at wit's end",
            "hyperventilating", "heart racing", "cold sweat",
        },

        "gratitude_appreciation": {
            "grateful", "thankful", "appreciative", "indebted", "blessed",
            "moved", "touched", "humbled", "honored", "privileged",
        },
    }

    total = sum(len(v) for v in results.values())
    print(f"    ✅ Added {total} manually curated emotion words/phrases")
    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("Emotional States Keyword Collector")
    print("=" * 60)

    # 先寫出指南
    with open("emotion_lexicons_guide.txt", "w", encoding="utf-8") as f:
        f.write(GUIDE_TEXT)
    print("📖 Guide saved to: emotion_lexicons_guide.txt")

    # 收集所有來源
    all_categories = {}

    # Source 1: NRC EmoLex
    nrc = get_nrclex_words()
    all_categories.update(nrc)

    # Source 2: AFINN
    afinn = get_afinn_words()
    all_categories.update(afinn)

    # Source 3: VADER
    vader = get_vader_words()
    all_categories.update(vader)

    # Source 4: 手動擴展
    manual = get_manual_emotion_words()
    all_categories.update(manual)

    # 合併輸出
    if all_categories:
        # CSV: 按類別分組
        rows = []
        for category, words in sorted(all_categories.items()):
            for word in sorted(words):
                rows.append({"category": category, "word": word})

        df = pd.DataFrame(rows)
        df.to_csv("emotion_keywords_by_category.csv", index=False, encoding="utf-8-sig")
        print(f"\n✅ CSV saved: emotion_keywords_by_category.csv")
        print(f"   Total entries (with categories): {len(df)}")

        # TXT: 所有不重複的詞
        all_words = set()
        for words in all_categories.values():
            all_words.update(words)

        with open("emotion_keywords_all.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(all_words)))
        print(f"   Total unique keywords: {len(all_words)}")
        print(f"   Keywords saved to: emotion_keywords_all.txt")

        # 統計
        print("\n📊 Summary by category:")
        print("-" * 50)
        for cat in sorted(all_categories.keys()):
            print(f"   {cat:35s} {len(all_categories[cat]):>6,}")
        print("-" * 50)
        print(f"   {'TOTAL UNIQUE':35s} {len(all_words):>6,}")

    print("\nDone! 🎉")
    print("\n💡 Next steps:")
    print("   1. 檢查 emotion_lexicons_guide.txt 了解各來源詳情")
    print("   2. 手動下載 NRC VAD Lexicon (20,000 詞 valence score):")
    print("      https://saifmohammad.com/WebPages/nrc-vad.html")
    print("   3. 如果學校有 LIWC 授權，加入 LIWC 的情緒分類")
    print("   4. 將 emotion_keywords_all.txt 餵入 keyword collector")


if __name__ == "__main__":
    main()
