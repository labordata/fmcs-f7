# Collective Bargaining Notice (F-7) Data from The Federal Mediation and Conciliation Service, 1997-Present

Daily refreshed data on [bargaining notices from fmcs.gov](https://www.fmcs.gov/resources/documents-and-data/#tab-d3d7f5344cef9bab4d3). Data is updated nightly at about 10:00 pm Eastern, though the 
FMCS ony updates their data monthly.

* [sqlite database](http://labordata.github.io/fmcs-f7/f7.db.zip)
* [CSV](http://labordata.github.io/fmcs-f7/f7.csv.zip)
* [online access](https://labordata.bunkum.us/f7)


## Industry coding

How a notice's industry is recorded changed over time:

* **2005–present:** the `naics` column holds a [NAICS](https://www.census.gov/naics/) code, and `industry` holds a spelled-out sector name.
* **1996–2004:** neither of those was used. Instead a single-letter FMCS industry
  code (`E`, `J`, `C`, `L`, …) was recorded. We move those legacy codes into
  their own column, **`industry_letter`**, so `industry` holds only the modern
  spelled-out names. The two taxonomies never co-occur on a record.

About 180,000 records (~34% of the database, all 1996–2004) carry only an
`industry_letter` and no NAICS.

### What the single-letter codes mean (best-guess crosswalk)

FMCS never published a legend for these codes. The mapping below is **inferred,
not official.** Using the companion
[bargaining-units panel](https://github.com/labordata/bargaining_units_f7), which
links repeat F-7 filings into bargaining units over time, we took units that
filed in *both* eras and read off which modern NAICS sector each old letter
turned into. The "NAICS-2 agreement" column is the share of that letter's later
filings whose 2-digit NAICS matches the guessed sector — treat it as a
confidence signal. (An independent crosswalk built by exact employer-name
matching gives the same answers, which is why we trust the high-confidence rows.)

| Code | Records | Best-guess sector | NAICS-2 agreement | Confidence |
|------|--------:|-------------------|-------------------|------------|
| `L` | 15,446 | Health Care & Social Assistance | 62 = 93% | High |
| `C` | 17,509 | Construction | 23 = 79% | High |
| `H` | 3,259 | Utilities | 22 = 77% | High |
| `E` | 54,714 | Manufacturing | 31–33 = 73% | High |
| `F` | 6,844 | Transportation & Warehousing | 48 = 69% | High |
| `U` | 5,967 | Retail Trade | 44–45 = 67% | High |
| `K` | 927 | Transportation & Warehousing | 48 = 66% | High |
| `S` | 2,635 | Educational Services | 61 = 50% | Medium |
| `G` | 2,848 | Information / Arts & Entertainment | 51 = 48%, 71 = 30% | Medium |
| `B` | 1,751 | Construction + Mining/Oil & Gas | 23 = 47%, 21 = 36% | Medium |
| `R` | 1,713 | Public Administration | 92 = 42% | Medium |
| `T` | 11,185 | mixed (Manufacturing + Retail) | 31 = 56%, 44 = 18% | Low |
| `D` | 1,175 | Manufacturing / Transportation (mixed) | 31 = 52%, 48 = 21% | Low |
| `J` | 51,473 | residual / "Services" catch-all (no dominant sector) | 56 = 25% (no plurality) | Low |
| `P` | 2,380 | Public Administration / Federal Government | 92 = 64% (few bridge) | Low |
| `A`, `Q`, `X`, `M`, `N`, `5` | < 270 each | too sparse to decode; likely data-entry noise | — | None |

Notes:

* `J` is the second-largest code but has no dominant successor sector — it looks
  like a generic residual bucket, so don't read it as one industry.
* `F` and `K` both map to Transportation & Warehousing (probably a sub-split,
  e.g. trucking vs. air/rail); `C` and `B` both involve Construction (`B` adds a
  strong Mining/Oil & Gas signal).
* `P` points cleanly at Public Administration, but very few `P` units survive
  into the NAICS era, so the sample is thin — hence Low confidence despite the
  high percentage.
* Because the crosswalk is probabilistic, it is documented here rather than
  baked into the data. The raw letter is preserved in `industry_letter` so you
  can apply your own mapping.

## Outcome of Initial Bargaining
This repository also includes public records requests about the outcome of initial bargaining.

* [Whether Initial Bargaining Lead to Contract, January 1, 2021 - June 9, 2022](https://www.muckrock.com/foi/united-states-of-america-10/whether-initial-bargaining-lead-to-contract-128794/#) 
  * [Spreadsheet](https://github.com/labordata/fmcs-f7/blob/main/raw/to_contract.csv)
