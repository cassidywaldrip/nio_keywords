# Assassination & Political Violence Keywords

A curated list of **356 unique keywords and phrases** related to assassination, political violence, coups, and political arrests. Designed for use in a keyword collector pipeline to detect discussions of political violence events in text data.

## Motivation

This keyword list was compiled to capture text related to events such as the 2024 Trump assassination attempts, the 2022 Shinzo Abe assassination, the 2022–2023 Brazilian coup plot, political leader arrests (e.g., Imran Khan, Bolsonaro indictment), and broader patterns of political violence worldwide.

## Data Source

Keywords were manually curated based on:
- Terminology used in news coverage of recent political violence events (2022–2026)
- Academic literature on political assassinations (e.g., Olken & Jones, 2009, "Hit or Miss? The Effect of Assassinations on Institutions and War")
- Legal and security terminology from government reports (e.g., DHS Independent Review of the 2024 Trump assassination attempt; House Task Force final report)
- Wikipedia's lists of assassinations, assassination attempts, and coups by country

## Files

| File | Description |
|------|-------------|
| `assassination_keywords.csv` | Full dataset with columns: `category`, `word`. 362 rows across 11 categories. |
| `assassination_keywords_list.txt` | Plain keyword list, one per line. 356 unique entries. Ready for keyword collector. |

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| `assassination_direct` | 19 | Core assassination terms: assassinate, assassination attempt, targeted killing, murder-for-hire, hitman, etc. |
| `attack_verbs` | 46 | Action verbs: shoot, stab, bomb, detonate, wound, poison, etc. |
| `weapons` | 44 | Weapons and tools: firearm, rifle, AR-15, explosive, IED, drone strike, nerve agent, Novichok, etc. |
| `coup_regime_change` | 45 | Coups and regime change: coup d'état, overthrow, oust, junta, insurrection, sedition, mutiny, etc. |
| `political_arrest_legal` | 47 | Legal/arrest terms for political figures: indict, arraign, impeach, extradite, house arrest, political prisoner, etc. |
| `political_violence_general` | 39 | Broader political violence: terrorism, extremism, mass shooting, hostage, kidnapping, martial law, etc. |
| `security_terms` | 26 | Security and protection: Secret Service, security breach, death threat, counter-sniper, bulletproof, etc. |
| `conspiracy_plot` | 21 | Planning and conspiracy: conspiracy, plot to kill, mastermind, accomplice, death squad, false flag, etc. |
| `aftermath_investigation` | 31 | Post-event terms: investigation, FBI, task force, suspect, gunman, motive, forensic, resignation, etc. |
| `historical_reference` | 20 | Names of notable assassination victims/events: JFK, Shinzo Abe, Benazir Bhutto, Soleimani, etc. |
| `international_operations` | 24 | State-level operations: drone strike, covert operation, extrajudicial killing, state-sponsored assassination, etc. |

## Notes

- Some keywords appear in multiple categories where they serve different functions (e.g., "bomb" in both `attack_verbs` and `weapons`).
- The `historical_reference` category contains proper nouns of well-known assassination victims; this list is intentionally selective rather than exhaustive — for comprehensive head-of-state names, see the separate head-of-state keyword list.
- Keywords are in English only. For multilingual keyword matching, consider translating the core terms.
