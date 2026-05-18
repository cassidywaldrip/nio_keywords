# Museums & Cultural Institutions Keywords

A global list of museum and cultural institution names from **Wikidata**, covering 31 institution types across all countries. Names are in English and local languages for use in a keyword collector pipeline.

## Data Source

All data is sourced from **Wikidata** ([wikidata.org](https://www.wikidata.org/)), a free, open knowledge base maintained by the Wikimedia Foundation. As of late 2025, Wikidata contains over 101,000 museum items alone. Data was retrieved via SPARQL queries against the Wikidata Query Service, paginated by institution type and continent to avoid timeout limits.

Names are retrieved in multiple languages (English, Chinese, French, German, Spanish, Italian, Japanese, Korean, Arabic, Russian, Portuguese, and others depending on region), satisfying the requirement for both English and local-language versions.

## Files

| File | Description |
|------|-------------|
| `cultural_institutions_sparql_queries.md` | SPARQL queries used to collect the data, organized by institution type and continent. Optimized to avoid Wikidata Query Service timeout. Can be re-run at [query.wikidata.org](https://query.wikidata.org/) to update the data. |
| `cultural_institutions_all.csv` | Complete dataset with columns: `wikidata_id`, `name_en`, `alt_names`, `country`, `type`. Deduplicated by Wikidata ID. |
| `cultural_institutions_keywords.txt` | Final keyword list — one name per line, deduplicated, including both English and local-language names. Ready for the keyword collector. |

## Institution Types Covered

| Category | Wikidata ID | Description |
|----------|-------------|-------------|
| **Museums** | | |
| Museum | Q33506 | General museums |
| Art museum | Q207694 | Fine arts, visual arts |
| History museum | Q2772772 | Historical museums |
| Science museum | Q2301048 | Science and technology |
| Natural history museum | Q2677461 | Natural history collections |
| Archaeological museum | Q4989906 | Archaeological artifacts |
| Military museum | Q1970365 | Military history |
| Children's museum | Q16735822 | Interactive children's exhibits |
| Ethnographic museum | Q15206070 | Ethnography and cultural heritage |
| Maritime museum | Q1473674 | Naval and maritime history |
| Open-air museum | Q575727 | Outdoor historical sites |
| Aviation museum | Q3658083 | Aviation and aerospace |
| Technology museum | Q1955659 | Technology and industry |
| Memorial museum | Q2772759 | Memorials and commemorations |
| **Performing Arts** | | |
| Opera house | Q153562 | Opera venues |
| Theater building | Q24354 | Theater and playhouse buildings |
| Concert hall | Q1060829 | Concert and recital halls |
| Performing arts center | Q17088587 | Multi-purpose performing arts venues |
| **Libraries & Archives** | | |
| National library | Q856234 | National-level libraries |
| Public library | Q28564 | Public lending libraries |
| Archive | Q166118 | Archival institutions |
| National archive | Q2860008 | National-level archives |
| **Galleries & Cultural Centers** | | |
| Art gallery | Q1007870 | Commercial and public galleries |
| Cultural center | Q18674739 | Community and national cultural centers |
| **Nature & Science** | | |
| Botanical garden | Q167346 | Botanical gardens and arboreta |
| Zoo | Q43229 | Zoological gardens |
| Aquarium | Q2281788 | Public aquariums |
| Planetarium | Q41176 | Planetariums |
| Science center | Q1292588 | Interactive science centers |
| **Festivals** | | |
| Film festival | Q220505 | Film and cinema festivals |
| Music festival | Q2153354 | Music festivals |
| Arts festival | Q868557 | General arts festivals |
| **Heritage** | | |
| UNESCO World Heritage Site | Q9259 | UNESCO-designated heritage sites |

## Notes

- Wikidata is a living database; results will vary slightly depending on when queries are run.
- The `alt_names` field in the CSV may contain names in dozens of languages, separated by commas.
- Some institutions appear under multiple Wikidata types (e.g., tagged as both `museum` and `art_gallery`). The output is deduplicated by `wikidata_id`.
- To update the data, re-run the SPARQL queries in `cultural_institutions_sparql_queries.md` at [query.wikidata.org](https://query.wikidata.org/) and download as CSV.
