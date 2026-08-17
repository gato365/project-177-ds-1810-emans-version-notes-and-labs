# STAT/DATA 1810 — Notes & Labs

Quarto website of in-class notes for STAT/DATA 1810 (Foundations + ETV cycles).
Each lesson has a student `.qmd` (blanks / chunks to insert) and an instructor
solution `.qmd`; the site renders both.

## Layout

```
_quarto.yml          site config (renders index.qmd + R/notes/**/*.qmd → docs/)
index.qmd            landing page: schedule table with KEY / STUDENT / .qmd links
styles/theme.scss    site theme
R/notes/week_N/...   *_empty.qmd (student) and *_solution.qmd (instructor key)
Data/                datasets read by the ETV cycles (paths are project-relative)
docs/                rendered site (GitHub Pages: Settings → Pages → main /docs)
_freeze/             cached chunk output (commit it; only changed docs re-run)
```

## Build

```sh
quarto render          # whole site → docs/
quarto preview         # live-reload while editing
```

Requires R with `tidyverse` and `readxl`.
