# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A flat collection of CSV files, each holding a keyword/name list for a single topic (e.g. country names, US senators, inflation-related vocabulary). There is no application code, build system, or tests — just data files. Each `.csv` is the artifact.

## Conventions

- Filenames are snake_case, end in `.csv`, and name the topic directly (e.g. `us_states_and_territories.csv`, `iran_war_words.csv`). Prefer accurate-to-contents names over short ones (the file was originally `us_states.csv` but was renamed once it also contained DC and territories).
- US-scoped lists are prefixed `us_` to distinguish them from global equivalents (`us_capital_cities.csv` vs. `world_capital_cities.csv`).
- Files start empty and are populated over time. Do not invent content — only add entries the user has supplied or explicitly asked you to gather.
- **Diacritic dual-form (bidirectional)**: whenever a name has both a diacritic and a non-diacritic form, include both as two rows with identical metadata in the other columns. Apply in both directions: if the source spells it with accents (`Côte d'Ivoire`), add the ASCII-stripped row (`Cote d'Ivoire`); if the source spells it without accents but a standard native diacritic form exists (`Sao Tome and Principe` → `São Tomé and Príncipe`), add the accented row. News-mention matching depends on both being present.
- **Variant rows map back to canonical English via column 2** (where the schema supports it). `country_names.csv` uses `Name,EnglishCountry,Region`: every variant row (ASCII-stripped, diacritic-restored, local-language, native script) carries the same Britannica-spelling canonical name in column 2 so a match resolves cleanly. Apply the same pattern when adding similar schemas to other files.
- **Local-language names**: include the dominant local form for each country/place. Non-Latin scripts written as-is (e.g. `日本`, `العراق`, `Россия`); no romanizations. For multi-language countries, one form only (the most-spoken or otherwise dominant) — don't dump every official translation.
- See `README.md` for the current per-file index (what's populated, what's still a placeholder).

## Working in this repo

- When the user asks for a "list of X," check whether a corresponding CSV already exists before creating a new file. Reuse the existing filename if there is one.
- When populating a file, ask the user about schema (single column vs. multiple columns, header row vs. no header, name variants/aliases) before writing rows — the existing files do not establish a schema yet.
- Several lists (governors, senators, house members, heads of state) are known to go stale quickly. Treat their contents as point-in-time and confirm the intended "as of" date before refreshing.

## Open questions (not yet resolved)

- `emotional_state_words.csv` exists as a placeholder; the user asked whether established dictionaries for emotional-state vocabulary exist before committing to a source. Do not populate without first surfacing candidate sources (e.g. NRC Emotion Lexicon, LIWC, GoEmotions) for the user to choose from.
- `cultural_institutions.csv` is intentionally broad ("other types of cultural institutions" beyond museums). Scope is undecided — confirm which categories are in/out before adding rows.
