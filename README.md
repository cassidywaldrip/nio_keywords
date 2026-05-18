# nio_keywords

Reference CSV files of keywords and names, one topic per file. The lists feed news/text mention-collection.

## Conventions

- One value per line, no header row, no quoting (no field currently contains a comma).
- Column schema depends on file. `country_names.csv` uses `Name,EnglishCountry,Region` — column 2 always holds the canonical English country (Britannica's spelling) so every variant maps back. Other multi-column files use the simpler `value,category` shape until a richer schema is needed.
- Names that have both a diacritic and a non-diacritic form appear as two paired rows — one of each — because source text uses both. Applies in both directions: if the source spells it `Côte d'Ivoire`, add `Cote d'Ivoire`; if the source spells it `Sao Tome and Principe`, add `São Tomé and Príncipe`.
- Local names (forms in the country's own language) live alongside English names as additional rows, each mapped back to the same canonical English country in column 2. Native scripts are written as-is (e.g. `日本`, `العراق`, `Россия`); romanizations are not included. For multi-language countries, only the dominant local form is stored.

## Files

### Populated

| File | Contents |
|---|---|
| `country_names.csv` | 368 rows, 3 columns (`Name,EnglishCountry,Region`). Country/territory list from [Britannica](https://www.britannica.com/topic/list-of-countries-1993160) with diacritic variants, ASCII variants, and dominant local-language names layered on top. Includes non-sovereign territories and contested entities (Kosovo, Taiwan, Gaza Strip, West Bank, Western Sahara) as listed in source. 63 rows are in non-Latin scripts (Arabic, Cyrillic, CJK, Devanagari, etc.) — see "Notes" for spot-check guidance. |
| `us_states_and_territories.csv` | 56 rows — 50 US states + District of Columbia + 5 inhabited US territories (American Samoa, Guam, Northern Mariana Islands, Puerto Rico, U.S. Virgin Islands). |
| `governors.csv` | 56 rows — 50 US states + District of Columbia + 5 inhabited US territories (American Samoa, Guam, Northern Mariana Islands, Puerto Rico, U.S. Virgin Islands). Governors pulled from [Wikipedia's List of US governors](https://en.wikipedia.org/wiki/List_of_current_United_States_governors). |
| `us_capital_cities.csv` | 57 rows, 2 columns (`City,State`). Capital cities for all 50 states + DC + 5 inhabited US territories, ordered to match `us_states_and_territories.csv`. One diacritic pair (Hagåtña/Hagatna for Guam). DC is listed with Washington as the capital city; Washington also appears once more as a state (capital Olympia). |
| `world_capital_cities.csv` | 280 rows, 2 columns (`City,Country`). National capitals from [Wikipedia's List of national capitals](https://en.wikipedia.org/wiki/List_of_national_capitals). Country names normalized to Britannica's spellings from `country_names.csv` (Ivory Coast → Côte d'Ivoire, Cape Verde → Cabo Verde, Palestine → West Bank, etc.). Includes Wikipedia's dependencies and breakaway/disputed territories (Abkhazia, Somaliland, Transnistria, Tristan da Cunha, etc.). Diacritic and ASCII variants paired for cities and country names where applicable. No local-language forms or romanizations (per user). |
| `heads_of_state.csv` | 243 rows, 3 columns (`Country,HeadOfState,HeadOfGovernment`). 195 sovereign states from [Wikipedia's List of current heads of state and government](https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government); 48 of them have a paired all-ASCII row for diacritic-bearing names (lockstep stripping — if any cell in a row has a diacritic, an all-stripped paired row follows). Country column normalized to Britannica's spellings from `country_names.csv`. When the same person holds both offices, both columns carry the identical name. Palestine kept as a separate entity (not in `country_names.csv`). |
| `senators.csv` | 99 rows, 2 columns (`Senator,State`). Current US senators from [Wikipedia's List of current US senators](https://en.wikipedia.org/wiki/List_of_current_United_States_senators). 100 senators expected (50 states × 2) — one row appears to be missing; spot-check before relying on completeness. |
| `house_members.csv` | 416 rows, 3 columns (`representative,state,district`), **with a header row** (the only file in this repo that does — keep the convention in mind if you join across files). Pulled from [house.gov/representatives](https://www.house.gov/representatives). Full House is 435 voting members + 6 non-voting delegates (DC, Puerto Rico, American Samoa, Guam, Northern Mariana Islands, US Virgin Islands) = 441; this list has 415 data rows, so ~26 seats unaccounted for (vacancies, missing delegates, or scraping gaps). District column is the integer number or `At Large` for single-seat states/territories. |

### Empty (planned)

| File | Intended contents |
|---|---|
| `assassination_words.csv` | Vocabulary related to assassination events. |
| `cultural_institutions.csv` | Cultural institutions beyond museums (libraries, archives, theaters, etc.). Scope TBD. |
| `emotional_state_words.csv` | Emotion vocabulary. Source lexicon (NRC, LIWC, GoEmotions, etc.) TBD. |
| `health_words.csv` | Health-related vocabulary, possibly grouped. |
| `inflation_words.csv` | Inflation-related vocabulary. |
| `iran_war_words.csv` | Vocabulary related to Iran-war coverage. |
| `major_cities.csv` | Major cities. Scope TBD (US-only vs. global). |
| `museums.csv` | Museum names. |

## Notes

- Officeholder lists (governors, senators, house members, heads of state) replace older lists that have gone stale; verify the "as of" date when populating.
- `emotional_state_words.csv` and `cultural_institutions.csv` should not be populated without first agreeing on a source/scope.
- Non-Latin script rows in `country_names.csv` should be spot-checked by a reader who can read the script. Less-common scripts (Tigrinya, Amharic, Dhivehi, Khmer, Lao, Burmese, Dzongkha, Sinhala) are most error-prone.
