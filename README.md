# STAT/DATA 1810 — Notes & Labs

**Live site:** https://gato365.github.io/project-177-ds-1810-emans-version-notes-and-labs/

Quarto website of in-class notes for STAT/DATA 1810 (Foundations + ETV cycles).
Each lesson has a student `.qmd` (blanks / chunks to insert) and an instructor
solution `.qmd`; the site renders both.

## Layout

```
_quarto.yml          site config (renders index.qmd + R/notes/**/*.qmd → docs/)
index.qmd            landing page: schedule table with KEY / STUDENT / .qmd links
styles/theme.scss    site theme
assets/             favicon.svg (source, edit this) + favicon.png (used by the site)
R/notes/week_N/...   *_empty.qmd (student) and *_solution.qmd (instructor key)
Data/                datasets read by the ETV cycles (paths are project-relative)
R/check_in/          weekly check-in quizzes: JSON → Word docs → explicit publish (see R/check_in/README.md)
docs/                rendered site (GitHub Pages: Settings → Pages → main /docs)
_freeze/             cached chunk output (commit it; only changed docs re-run)
```

## Build

```sh
quarto render          # whole site → docs/
quarto preview         # live-reload while editing
```

Requires R with `tidyverse` and `readxl`.
 
## Check-in quizzes

Questions live in `R/check_in/check_in_{self,collab}/week_NN.json`. 
Build the Word docs with `python R/check_in/scripts/build_checkins.py --week NN`
(output is git-ignored). 

**Nothing reaches the website until you run**
`python R/check_in/scripts/publish_checkin.py --week NN --type self --version blank`
(and, separately, `--version solution`). Full workflow: [R/check_in/README.md](R/check_in/README.md).

## Vertical space between headers (`vspace`)

Quarto collapses the gap between an `#` section and the `##` right after it.
To add breathing room anywhere in a `.qmd`, drop in the shortcode:

```
{{< vspace >}}            <!-- 2rem -->
{{< vspace 1.5rem >}}     <!-- any CSS length -->
```

It renders as an empty block (HTML) or `\vspace{}` (PDF) — never as text.
The extension lives in `_extensions/vspace/` and is registered in `_quarto.yml`.

**The "button":** in Positron/VS Code, type `vspace` (or `vs`) on a blank line
and press **Tab** — the snippet in `.vscode/quarto.code-snippets` expands it and
lets you Tab through the size choices. To put it on a key, add to your user
`keybindings.json`:

```json
{ "key": "cmd+alt+v", "command": "editor.action.insertSnippet",
  "when": "editorTextFocus && editorLangId == 'quarto'",
  "args": { "name": "Vertical space (vspace shortcode)" } }
```
