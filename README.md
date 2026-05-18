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
| `country_names.csv` | 243 rows, 3 columns (`country_name,english_name,region`). Country/territory list from [Britannica](https://www.britannica.com/topic/list-of-countries-1993160) with diacritic variants and dominant local-language names. Includes non-sovereign territories and contested entities (Kosovo, Taiwan, Gaza Strip, West Bank, Western Sahara, Palestine). |
| `us_states_and_territories.csv` | 57 rows (`state`) — 50 US states + District of Columbia + 5 inhabited US territories (American Samoa, Guam, Northern Mariana Islands, Puerto Rico, U.S. Virgin Islands). |
| `governors.csv` | 57 rows, 2 columns (`governor,state`) — 50 US states + District of Columbia + 5 inhabited US territories (American Samoa, Guam, Northern Mariana Islands, Puerto Rico, U.S. Virgin Islands). Governors pulled from [Wikipedia's List of US governors](https://en.wikipedia.org/wiki/List_of_current_United_States_governors). |
| `us_capital_cities.csv` | 59 rows, 2 columns (`city,state`). Capital cities for all 50 states + DC + 5 inhabited US territories, ordered to match `us_states_and_territories.csv`. Two diacritic pairs (Hagåtña/Hagatna for Guam, St. Paul for Saint Paul). |
| `world_capital_cities.csv` | 279 rows, 2 columns (`city,country`). National capitals from [Wikipedia's List of national capitals](https://en.wikipedia.org/wiki/List_of_national_capitals). Includes Wikipedia's dependencies and breakaway/disputed territories (Abkhazia, Somaliland, Transnistria, Tristan da Cunha, etc.). Diacritic and ASCII variants paired for cities and country names where applicable. No local-language forms. |
| `heads_of_state.csv` | 244 rows, 3 columns (`country,head_of_state,head_of_government`). 195 sovereign states from [Wikipedia's List of current heads of state and government](https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government); 48 of them have a paired all-ASCII row for diacritic-bearing names (lockstep stripping — if any cell in a row has a diacritic, an all-stripped paired row follows). Country column normalized to Britannica's spellings from `country_names.csv`. When the same person holds both offices, both columns carry the identical name. |
| `senators.csv` | 101 rows, 2 columns (`senator,state`). Current US senators from [Wikipedia's List of current US senators](https://en.wikipedia.org/wiki/List_of_current_United_States_senators). |
| `house_members.csv` | 436 rows, 3 columns (`state,district,representative`). Pulled from [Wikipedia's list of current US representatives](https://en.wikipedia.org/wiki/List_of_current_United_States_representatives). |

### Empty (planned)

| File | Intended contents |
|---|---|
| `assassination_words.csv` | Vocabulary related to assassination events. |
| `cultural_institutions.csv` | Cultural institutions beyond museums (libraries, archives, theaters, etc.). Scope TBD. |
| `emotional_state_words.csv` | Emotion vocabulary. Source lexicon (NRC, LIWC, GoEmotions, etc.) TBD. |
| `health_words.csv` | Health-related vocabulary, possibly grouped. |
| `inflation_words.csv` | Inflation-related vocabulary. |
| `iran_war_words.csv` | Vocabulary related to Iran-war coverage. |
| `major_cities.csv` | Major world cities. |
| `museums.csv` | Museum names. |
