# Check-In Quizzes — DATA 1810

Weekly **Self** and **Collaborative** check-ins. Questions live in JSON; a Python
script turns each JSON into three Word documents (blank / solution / rubric);
a second script is the *only* way any document reaches the public website.

```
R/check_in/
├── check_in_self/      week_NN.json   ← SOURCE (you edit these)
├── check_in_collab/    week_NN.json   ← SOURCE (you edit these)
├── templates/format.json              ← fonts, margins, header line, labels
├── scripts/build_checkins.py          ← JSON → .docx
├── scripts/publish_checkin.py         ← explicit release / unrelease
├── generated/                         ← BUILT .docx  (git-ignored, never deployed)
├── public/                            ← RELEASED .docx + manifest.json (committed, deployed)
└── checkins.qmd                       ← website page (generated — don't hand-edit)
```

## Weekly workflow (the short version)

1. Copy last week's JSON → `week_NN.json`, edit questions / answers / rubrics / points
2. `python R/check_in/scripts/build_checkins.py --week NN`
3. Print `generated/week_NN/self/week_NN_self_blank.docx` for class
4. After class: `publish_checkin.py --week NN --type self --version blank`
5. When students should see answers: `publish_checkin.py --week NN --type self --version solution`
6. `quarto render` → `git add -A && git commit && git push`

Nothing in step 2 touches the website. Only step 4/5 + 6 do.

---

## Creating a new week

```sh
cp R/check_in/check_in_self/week_01.json   R/check_in/check_in_self/week_02.json
cp R/check_in/check_in_collab/week_01.json R/check_in/check_in_collab/week_02.json
```

Then edit both files:

- `week` → `2`, `title` → `"Week 2 Self Check-In"` (the file name and the `week` field must agree)
- every question `id` → `self_w02_q01`, … (ids must be unique within a file)
- `question`, `answer`, `rubric`, `instructor_notes`, `points`
- leave `blank_published` / `solution_published` as `false` — the publish script flips them

Question fields:

| field | meaning |
|---|---|
| `id` | unique string, e.g. `collab_w02_q03` |
| `type` | `short_answer` · `multiple_choice` · `true_false` · `code` |
| `question` | text shown to students; paragraphs separated by a blank line; lines starting with 4 spaces render as code |
| `points` | number, or `null` if undecided |
| `extra_credit` | `true` marks it `[EC]` and keeps it out of the main total |
| `answer` | model answer (solution + rubric only) |
| `rubric` | how to award credit (rubric only) |
| `instructor_notes` | optional grading notes (solution only) |
| `answer_space_inches` | blank space under the question in the blank version |

Quiz-level fields: `title`, `version` (A/B/C), `time_limit`, `instructions`
(`{time_limit}` is substituted and bolded).
Optional `total_points` pins the stated total (intro sentence and rubric `Total:` line)
regardless of what the question points add up to — use it when the blank that students
received already states a total (e.g. after a hand edit) so solution/rubric match it.

### Multiple versions of one quiz

`week_NN.json` is version A. Add `week_NN_B.json`, `week_NN_C.json` (same `week`,
`version: "B"` / `"C"`) for alternates. `--week NN` builds all of them; the extra
versions get a letter in the file name:

```
generated/week_01/collab/week_01_collab_blank.docx      ← A
generated/week_01/collab/week_01_collab_B_blank.docx    ← B
generated/week_01/collab/week_01_collab_C_blank.docx    ← C
```

Several versions in ONE document (page break between them):

```sh
python R/check_in/scripts/build_checkins.py --week 1 --type collab --combine B C --versions solution rubric
# -> generated/week_01/collab/week_01_collab_BC_{solution,rubric}.docx
```

A quiz JSON may set `"header_line"` to override the page header from `format.json`
(e.g. `Group Number:` instead of `Cal Poly username:` for collaborative quizzes).

(`publish_checkin.py` currently handles version A only.)

### Red ink in solutions

In the solution version, *Model answer* and *Instructor notes* are printed in red
(`solution_ink_hex` in `templates/format.json`, default `EE0000`). Edit the JSON, not
the built `.docx` — a rebuild overwrites any hand edits.

## Setting points

Edit `"points"` on each question — **that is the only place points live**:

```json
{ "id": "self_w01_q01", "points": 1.5, ... }
{ "id": "self_w01_q05", "points": 0.75, "extra_credit": true, ... }
```

- `null` → renders as `(__ PTS)` and the total as `__`, with a warning at build time
- The intro sentence ("This quiz is worth **N points** total. The extra credit question is worth **M points**.") is computed from the JSON

## Building documents

```sh
python R/check_in/scripts/build_checkins.py --week 1                  # self + collab, all 3 versions
python R/check_in/scripts/build_checkins.py --week 1 --type self
python R/check_in/scripts/build_checkins.py --week 1 --type collab
python R/check_in/scripts/build_checkins.py --week 1 --versions blank  # just the student copy
python R/check_in/scripts/build_checkins.py --all                      # every week found
```

Output → `R/check_in/generated/week_01/{self,collab}/week_01_<type>_{blank,solution,rubric}.docx`

The JSON is validated first; the build refuses and tells you exactly what's wrong
for: missing/duplicate ids, empty question/answer/rubric, bad `points`, unknown
`type`, invalid `check_in_type`, malformed JSON. Warnings (not errors): `null`
points and leftover `[INSTRUCTOR …]` placeholders.

Formatting (Garamond 11 pt, 1" margins, Name / Cal Poly username / Date header on
every page, `Q1. (1.5 PTS)` labels, `[EC]` prefix) follows the Quiz 12 spec and is
set in `templates/format.json`. Requires `pip install python-docx`.

## Publishing (explicit trigger)

```sh
python R/check_in/scripts/publish_checkin.py --week 1 --type self --version blank
python R/check_in/scripts/publish_checkin.py --week 1 --type self --version solution   # later, separately
python R/check_in/scripts/publish_checkin.py --status
```

Each call:

1. copies the built `.docx` from `generated/` → `public/week_01/`
2. sets `blank_published` / `solution_published: true` in the source JSON
3. records it in `public/manifest.json`
4. regenerates `checkins.qmd` with a download link

Then `quarto render` and commit/push. **Blank and solution are independent** —
publishing the blank never exposes the solution. Rubrics are refused outright.

## Unpublishing

```sh
python R/check_in/scripts/publish_checkin.py --week 1 --type self --version solution --unpublish
quarto render
git add -A && git commit -m "unpublish week 1 self solution" && git push
```

This deletes the file from `public/` **and** from the rendered `docs/`, resets the
JSON flag, and removes the link. The push is what removes it from GitHub Pages.
(If it was live, assume someone may have downloaded it.)

## Git / GitHub safety

| path | status | commit? | deployed? |
|---|---|---|---|
| `check_in_self/*.json`, `check_in_collab/*.json` | **private source** (contains answers) | yes — it's your backup | no |
| `templates/`, `scripts/` | code | yes | no |
| `generated/**` | built instructor docs | **no** (git-ignored) | no |
| `public/**` | explicitly released docs + manifest | yes | **yes** |
| `checkins.qmd` | generated page | yes | yes (rendered) |
| `docs/R/check_in/**` | rendered output | yes | **yes** — this *is* the site |

Safeguards in place:

- `generated/` is git-ignored, so built solutions/rubrics can't be committed by accident
- `*_rubric.docx` is git-ignored everywhere under `public/` as a second lock
- Quarto copies only `R/check_in/public/**/*.docx` into the site (`_quarto.yml` → `resources`); it never renders or copies `generated/`
- Audit any time: `python R/check_in/scripts/publish_checkin.py --check` — exits non-zero if `docs/` contains any `.docx` not in the manifest

**Important:** the JSON files contain answers. They are committed (so you have a
backup) but are only private if the **GitHub repository is private**. If this repo
is public, GitHub Pages hides nothing in the *repo* — only `docs/` is the site, but
the JSON would be browsable on github.com. Either keep the repo private or move
the JSON to a private repo and point `SOURCE_DIRS` in the scripts at it.
