# Emotional States Keywords

A collection of **13,041 unique emotion-related words and phrases**, compiled from multiple NLP sentiment/emotion lexicons and manually curated vocabulary lists. Designed for use in a keyword collector pipeline.

## Data Sources

| Source | Description | Words | What It Provides |
|--------|-------------|-------|------------------|
| **NRC EmoLex** (v0.92) | NRC Word-Emotion Association Lexicon (Mohammad & Turney, 2013). Crowdsourced via Amazon Mechanical Turk. | ~14,000 | 8 emotion categories (anger, anticipation, disgust, fear, joy, sadness, surprise, trust) + positive/negative sentiment |
| **AFINN-111** | Valence lexicon manually labeled by Finn Årup Nielsen (2009–2011). | ~2,500 | Integer valence scores from −5 (most negative) to +5 (most positive) |
| **VADER** | Valence Aware Dictionary and sEntiment Reasoner (Hutto & Gilbert, 2014). Built for social media text. | ~7,500 | Valence scores from −4 to +4; includes emoji, slang, and acronyms |
| **Manual curation** | Hand-picked emotion vocabulary organized by Plutchik's Wheel of Emotions, supplemented with psychological states commonly used in ESL/EFL teaching materials. | ~440 | Fine-grained categories not covered by the above (e.g., shame, jealousy, boredom, loneliness, stress) |

## Files

| File | Description |
|------|-------------|
| `emotion_keywords_final.txt` | **Primary output.** 13,041 unique keywords, one per line. Ready to feed into a keyword collector. |
| `emotion_keywords_merged.csv` | Full dataset with columns: `category`, `word`, `source`. 25,229 rows (a word can appear in multiple categories). |
| `emotion_keywords_with_all_categories.csv` | Lookup table with columns: `word`, `categories`. Each word is mapped to all of its associated emotion labels (comma-separated). 13,041 rows. |
| `nrc_emolex_by_emotion.csv` | Raw NRC EmoLex data with columns: `emotion`, `word`. |
| `emotion_keywords_by_category.csv` | AFINN + VADER + manual curation data with columns: `category`, `word`. |
| `fetch_emotion_keywords.py` | Python script that downloads AFINN and VADER lexicons, adds manually curated words, and outputs the merged CSV and keyword list. |
| `fix_nrclex.py` | Helper script that loads NRC EmoLex through multiple fallback methods (local file → GitHub download → NRCLex API). |

## Category Reference

**NRC EmoLex categories** (prefixed with `nrc_` in the merged file):

`nrc_anger` · `nrc_anticipation` · `nrc_disgust` · `nrc_fear` · `nrc_joy` · `nrc_sadness` · `nrc_surprise` · `nrc_trust` · `nrc_positive` · `nrc_negative`

**AFINN/VADER categories** (grouped by valence intensity):

`afinn_very_negative` · `afinn_negative` · `afinn_positive` · `afinn_very_positive` · `vader_very_negative` · `vader_negative` · `vader_positive` · `vader_very_positive`

**Manually curated categories** (based on Plutchik + additional psychological states):

`joy_extended` · `sadness_extended` · `anger_extended` · `fear_extended` · `surprise_extended` · `disgust_extended` · `trust_extended` · `anticipation_extended` · `love_affection` · `pride_confidence` · `shame_guilt` · `confusion_uncertainty` · `boredom_apathy` · `jealousy_envy` · `loneliness_isolation` · `stress_anxiety` · `gratitude_appreciation`

## How to Reproduce

```bash
pip install requests pandas nrclex afinn vaderSentiment
python fetch_emotion_keywords.py   # generates AFINN + VADER + manual keywords
python fix_nrclex.py               # generates NRC EmoLex keywords
# then merge the two outputs (see fetch_emotion_keywords.py for details)
```

## Citations

- Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a Word–Emotion Association Lexicon. *Computational Intelligence*, 29(3), 436–465.
- Nielsen, F. Å. (2011). A New ANEW: Evaluation of a Word List for Sentiment Analysis in Microblogs. *Proceedings of the ESWC2011 Workshop on Making Sense of Microposts*, 93–98.
- Hutto, C. J., & Gilbert, E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. *Proceedings of the Eighth International AAAI Conference on Weblogs and Social Media*.
