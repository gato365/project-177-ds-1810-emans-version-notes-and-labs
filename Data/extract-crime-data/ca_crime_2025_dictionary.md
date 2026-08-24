# Data dictionary — `ca_crime_2025.rda`

**Source:** FBI National Incident-Based Reporting System, 2025 master file
(national file accepted through March 2026), filtered to California
(NIBRS numeric state code `4`).

**Built by:** `00_build_ca_nibrs_2025.qmd`

**Loading:** `load("data/ca_crime_2025.rda")` — drops four data frames into the
environment. `load()` does not return a value; do not assign it.

> **Verify before distributing.** This is the *specified* schema — what the
> build script is written to produce. The build script's §6 auto-generates the
> real one from the actual objects (`ca_crime_2025_dictionary.csv`), including
> row counts, missingness, and distinct-value counts. Trust that file over this
> one where they disagree, and diff them after every rebuild.

---

## `ca_offense`

**Grain:** one row per **offense record**. An incident with three offenses
contributes three rows sharing one `ori` + `incident_number`.

| Variable | Type | Description |
|---|---|---|
| `ori` | character | Originating Agency Identifier, 9 chars. Uniquely identifies a police department. Join key to `ca_agency`. |
| `agency` | character | Department city name, title-cased. |
| `incident_number` | character | Incident ID. **Unique only within an agency** — always join on `ori` *and* `incident_number`. |
| `incident_date` | Date | Date the offense occurred. Parsed from `YYYYMMDD`. |
| `month` | factor | Month abbreviation, ordered Jan–Dec. Derived. |
| `weekday` | factor | Day name, ordered Monday–Sunday. Derived. |
| `crime_cat` | factor | Broad offense category (e.g. Assault Offenses). |
| `crime` | factor | Specific offense (e.g. Aggravated Assault). |
| `ucr_offense_code` | character | Raw 3-char UCR code (e.g. `13A`). Kept for joining to external references. |
| `completed` | factor | `Attempted` / `Completed`. |
| `location` | factor | Location type (e.g. Residence/Home, Highway/Road/Alley). |
| `firearm` | logical | `TRUE` if a firearm code (11 firearm type not stated, 12 handgun, 13 rifle, 14 shotgun, 15 other firearm) appears in any of the three weapon fields. Matched on the leading two digits, because `weapon_force_2`/`_3` are 3 chars wide and may carry an automatic-weapon indicator (`12A`). Derived. |
| `bias` | logical | `TRUE` if a bias motivation other than "none" was recorded. Derived. |
| `arrest_made` | logical | `TRUE` if any arrest record exists for this incident. **Right-censored — see caveats.** |
| `days_to_arrest` | numeric | Days from offense to earliest arrest. `NA` when no arrest. Negative values set to `NA`. |
| `cleared_60` | logical | `TRUE` if an arrest occurred within 60 days. **Use this, not `arrest_made`, for cross-month comparison.** |

---

## `ca_victim`

**Grain:** one row per victim per incident. Includes non-person victims
(businesses, society) — filter on `victim_type == "Individual"` for demographics.

| Variable | Type | Description |
|---|---|---|
| `ori` | character | Agency identifier. Join key. |
| `incident_number` | character | Incident ID. Join key. |
| `victim_seq` | integer | Victim sequence number within the incident. |
| `victim_type` | factor | Individual, Business, Financial institution, Government, Religious organization, Society/Public, Law enforcement officer, Other, Unknown. |
| `age` | numeric | Age in years. `NA` for non-person victims and non-numeric age codes. |
| `sex` | factor | Female, Male. `NA` otherwise. |
| `race` | factor | White, Black, American Indian/Alaska Native, Asian, Native Hawaiian/Pacific Islander, Unknown. |
| `ethnicity` | factor | Hispanic or Latino, Not Hispanic or Latino, Unknown. |
| `ucr_offense_code` | character | First offense code this victim was connected to. NIBRS stores up to ten; **only the first is retained here.** |
| `relationship` | character | 2-char code for victim's relationship to offender (e.g. `SB` sibling, `AQ` acquaintance). Undecoded. |

---

## `ca_arrestee`

**Grain:** one row per arrested person per incident.

| Variable | Type | Description |
|---|---|---|
| `ori` | character | Agency identifier. Join key. |
| `incident_number` | character | Incident ID. Join key. |
| `arrest_date` | Date | Date of arrest. |
| `arrest_type` | factor | On-view, Summoned/cited, Taken into custody. |
| `ucr_arrest_offense_code` | character | Raw UCR code for the arrest offense. |
| `arrest_crime` | factor | Decoded arrest offense. |
| `age` | numeric | Age at arrest. |
| `sex` | factor | Female, Male. |
| `race` | factor | Same levels as `ca_victim$race`. |
| `ethnicity` | factor | Same levels as `ca_victim$ethnicity`. |

> Arrestee sequence numbers do **not** correspond to offender sequence
> numbers. You cannot line up arrestees with offenders by sequence.

---

## `ca_agency`

**Grain:** one row per California law enforcement agency. Agencies that report
through another agency (`covered_by_ori` non-missing) are excluded, so
populations do not double-count.

| Variable | Type | Description |
|---|---|---|
| `ori` | character | Agency identifier. Primary key. |
| `agency` | character | City/agency name, title-cased. |
| `population` | numeric | Population covered. Summed across counties for agencies spanning several. `NA` if zero/unrecorded. |
| `reports_nibrs` | logical | `TRUE` if the agency submitted to NIBRS. **`FALSE` is the coverage-gap flag.** |
| `months_reported` | integer | Months reported, 0–12. `NA` for out-of-range values in the source. |
| `full_year` | logical | `TRUE` if `months_reported == 12`. |

---

## Joining

```r
# offense -> agency (many-to-one)
ca_offense |> left_join(ca_agency, by = "ori")

# offense -> victim (many-to-many at incident level)
ca_offense |> left_join(ca_victim, by = c("ori", "incident_number"))
```

The offense–victim join is **many-to-many**. An incident with 2 offenses and 3
victims produces 6 rows. NIBRS does not link a specific victim to a specific
offense at this level of detail, so those 6 rows describe co-occurrence, not
correspondence. Aggregate to the incident before joining if you need clean
counts.

---

## Caveats that change conclusions

**1. Coverage.** About 80% of California's population lived in a
NIBRS-reporting jurisdiction in 2025 — among the lowest state coverage rates
nationally. Statewide totals computed from this file are undercounts of
unknown, non-uniform size. Compute the covered denominator from `ca_agency`
and report it alongside any total.

**2. Right-censoring.** Submissions closed March 2026. A January offense had
~14 months to accrue an arrest record; a December offense had ~3. `arrest_made`
therefore declines through the year for a reason that has nothing to do with
crime or policing. `cleared_60` gives every offense the same 60-day window and
is the comparable measure.

**3. Reported crime only.** Reporting propensity varies by offense type, victim
characteristics, and geography. Comparing counts across crime types compares
reporting behavior as much as incidence.

**4. Offense records ≠ incidents ≠ crimes.** `nrow(ca_offense)` counts offense
records. Use `n_distinct(paste(ori, incident_number))` for incidents.

**5. Teaching subset.** `ca_crime_2025.rda` contains a selected set of agencies,
not all of California. `ca_crime_2025_full.rda` (instructor-only) has the full
state. Check `n_distinct(ca_offense$ori)` before generalizing.

**6. Recency.** This is calendar year 2025. The national NIBRS file lags roughly
eight to nine months behind the year it covers. For current-month data, use a
city open-data portal instead.

---

## Provenance

| Item | Value |
|---|---|
| Source | FBI Crime Data Explorer, NIBRS 2025 national master file |
| Filter | `state = 4` (California) |
| Pipeline | R4crim Ch. 5 (CC-BY-SA, Greg Ridgeway) → SQLite → SQL extract → dplyr transform |
| Lookup tables | `gregridgeway/R4crim`, `NIBRS/` folder |
| Build script | `00_build_ca_nibrs_2025.qmd` |
| Rebuild cadence | Annual, when the FBI posts the next master file (~Sept) |
