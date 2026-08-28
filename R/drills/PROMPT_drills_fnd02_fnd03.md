# Prompt — generate drill questions for Foundations 02 & 03

Paste everything below the line into your AI of choice, attaching (or pasting)
`fnd02_types_structures_solution.qmd` and `fnd03_inspect_access_solution.qmd`.
Drills are graded for **completion**, ~10 questions each, 5–20 minutes, ~4 per
week (syllabus §7/§8).

---

You are writing **drill questions** for STAT/DATA 1810 (Data Science I, Cal
Poly), an introductory R course taught in Positron with Quarto. Drills are
short, low-stakes practice sets graded for completion, so they should be
**many, small, and immediately checkable** — not clever.

## Source material (attached)
- **Foundations 02 — Data Types and Data Structures.** Types defined first
  (numeric/double, integer, character, logical, factor, Date/date-time, NA),
  then discovered with `class()` / `typeof()`; the three families
  (quantitative / categorical / other = date-time); the string-vs-character
  distinction; factors vs characters (levels, order, values-not-on-the-menu
  become `NA`); coercion in `c()`; vectors, data frames vs tibbles (`tibble()`,
  `tribble()`), lists, matrices; `is.na()` + `sum()`. Error families: coercion,
  mismatched column lengths, factor level typo → silent `NA`.
- **Foundations 03 — Inspecting and Accessing Data.** `head/tail/dim/nrow/
  ncol/names/str/glimpse/summary`; "what is one row?"; `$`, `[rows, cols]`,
  `[[ ]]` (kept light); the native pipe `|>` read as "and then", one step per
  line, fills only the first argument; storage units byte→KB→MB→GB→TB with
  real-world anchors and `object.size()`; R holds data in memory. Error
  families: `$` typo → silent `NULL`, wrong name in `[ ]` → loud error, broken
  pipe → error one line late.

## Course learning outcomes these drills must exercise
- CLO 1.4 assignment · 1.5 data types · 1.6 containers (vector, data frame/
  tibble, list) · 1.12 storage magnitudes
- CLO 7.4 comparison operators · 7.6 `is.na()`
- CLO 11.1 reading help pages
Tag every question with the sub-outcome(s) it hits.

## Context rules
- Use **Cal Poly / San Luis Obispo** examples the way the lessons do: lattes
  at Julian's, the UU Starbucks, and Scout Coffee (prices, sizes, iced);
  Rec Center headcounts by time slot (morning/afternoon/evening); places to
  eat near campus; games vs. UCSB; miles from campus. Built-in datasets
  allowed: `airquality`, `iris`, `mtcars` only.
- Load **only** `library(tibble)` when a package is needed. Never
  `library(tidyverse)`. No dplyr/ggplot2 — those start next week.
- Use the **native pipe `|>`**, never `%>%`.
- Students insert their own chunks (Cmd/Ctrl + Shift + I); do not explain
  how.

## What to produce
Four drills, **10 questions each**, in this order:

1. **Drill A — Types & families** (Fnd 02 §1): predict `class()`, sort
   variables into quantitative / categorical / other, string vs character,
   factor vs character (levels, order, the silent `NA`), `is.na()` counting.
2. **Drill B — Structures** (Fnd 02 §2): build vectors/tibbles/lists from a
   description, predict coercion in `c()`, read tibble printouts (`<chr>`,
   `<dbl>`, `<fct>`, `3 × 2`), spot the one bug in a `tibble()` call, list vs
   vector.
3. **Drill C — Inspect & access** (Fnd 03 §1–2): given `glimpse()` /
   `summary()` output, answer rows/columns/one-row/NAs; write the `$` /
   `[ ]` line for a described piece; `sum(x > k)` and `sum(is.na(x))`;
   `nrow()` inside brackets; `$` vs `[ ]` vs `[[ ]]` return types.
4. **Drill D — Pipe & size** (Fnd 03 §3–4): rewrite nested calls as pipes and
   back, read a pipe as an "and then" sentence, identify the broken-pipe bug,
   where `na.rm = TRUE` goes; storage ladder conversions (KB↔MB↔GB), pick the
   right unit for a described object, "does it fit in 8 GB?" reasoning,
   `object.size()` scaling by rows.

Within each drill use a **mix of formats**: ~4 multiple choice (5–6 options,
plausible distractors that reflect real misconceptions), ~2 numeric answer,
~2 "write one line of code", ~2 "predict the output / spot the bug and name
its error family". At least **two questions per drill** should be *silent
failure* items — code that runs without a red error and gives a wrong answer
(coercion, factor typo → `NA`, `$` typo → `NULL`).

## Format for every question
```
### A3  [CLO 1.5]  (mc)
Question text. Code in fenced ```r blocks.
Options: a) … b) … c) … d) … e) …
Answer: b
Why: one sentence a student can learn from.
Common wrong answer: which option and why students pick it.
```
For numeric items give the exact value and a tolerance; for code items give
one canonical answer and any accepted equivalents.

## Constraints
- Every code snippet must actually run in R 4.x with only base R + tibble,
  and every stated output must be correct — compute it, don't guess
  (e.g. `mean(airquality$Ozone, na.rm = TRUE)` = 42.13; `sum(is.na(
  airquality$Ozone))` = 37; `object.size(airquality)` = 5,632 bytes;
  `object.size(iris)` = 7,256 bytes).
- Difficulty: 70% direct recall/application of the lesson, 30% one-step
  transfer to a new Cal Poly example. Nothing that requires content not in
  the two attached files.
- Keep each question answerable in under two minutes.
- Output the four drills as a single Markdown document with an answer key
  section per drill at the end.
