#!/usr/bin/env python3
"""
Lab 01 Canvas quiz builder — STAT/DATA 1810.

Posts the Lab 01 quiz directly to Canvas through the Canvas API (canvasapi),
and writes a human-readable answer key next to this script.

The quiz gates Lab 01: some questions ask for values students produced in the
.qmd, and the rest test the concepts the lab covers (Positron panes, assignment,
packages vs. libraries, data types vs. structures, NA handling, tibbles vs.
data frames, memory/storage, reproducible rendering).

SETUP (one time):
    pip install canvasapi python-dotenv

    Project-root .env must contain:
        CANVAS_API_KEY=your_token_here
    Optional overrides (defaults shown):
        CANVAS_API_URL=https://canvas.calpoly.edu
        CANVAS_COURSE_ID=192205

USAGE:
    python3 make_canvas_quiz.py --dry-run   # print payloads, post nothing
    python3 make_canvas_quiz.py             # create quiz as an unpublished draft
    python3 make_canvas_quiz.py --publish   # create and publish immediately

Quiz settings: 15 questions, 3 attempts (highest kept), 120-minute time limit.
"""

import argparse
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent


def _find_project_root() -> Path:
    for p in [HERE, *HERE.parents]:
        if (p / ".env").exists() or (p / ".git").exists():
            return p
    return HERE


ROOT_DIR = _find_project_root()

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass  # fine if the vars are already exported in the shell

API_URL   = os.getenv("CANVAS_API_URL", "https://canvas.calpoly.edu").rstrip("/")
API_KEY   = os.getenv("CANVAS_API_KEY")
COURSE_ID = int(os.getenv("CANVAS_COURSE_ID", "192205"))

# ---------------------------------------------------------------------------
# Quiz metadata
# ---------------------------------------------------------------------------
QUIZ_TITLE = "Lab 01 Quiz — Foundations"
QUIZ_DESCRIPTION = (
    "<p>Complete the Lab 01 Quarto document first. Several questions ask for "
    "values and answers you produced there; the rest test the concepts the lab "
    "covers. You must render your .qmd to HTML and Word before taking this quiz.</p>"
    "<p>3 attempts, 2 hours each. Your highest score is kept.</p>"
)
ALLOWED_ATTEMPTS = 3
TIME_LIMIT_MIN   = 120
SHUFFLE_ANSWERS  = False   # keep answer order as written

# ---------------------------------------------------------------------------
# Questions
#   type "mc"  -> multiple choice, ONE correct  (choices, answer = index)
#   type "ma"  -> multiple answers, SEVERAL correct (choices, answer = [indices])
#   type "num" -> numerical, exact answer (answer, tol)
# Every mc/ma item has at least 5 choices.
# ---------------------------------------------------------------------------
QUESTIONS = [
    # ---- Part A · Positron & the environment -----------------------------
    dict(type="mc", points=1, source="Lab Q1",
         text="In Positron, which pane answers one command at a time and forgets "
              "that command when the session ends?",
         choices=["Source editor", "Console", "Variables", "Help", "Plots", "Terminal"],
         answer=1),

    dict(type="mc", points=1, source="Lab Q3 (concept)",
         text="Why did <code>wheels</code> keep its value after you changed "
              "<code>cars_counted</code> in the Console?",
         choices=[
             "R updates objects automatically only inside chunks, not in the Console",
             "Assignment stores the <em>result</em> of the calculation at the moment it "
             "runs; <code>wheels</code> is not linked to <code>cars_counted</code> afterward",
             "Objects created inside a chunk are locked until the document is rendered",
             "<code>wheels</code> is a constant because it was created with <code>*</code>",
             "The Console and the Variables pane use separate memories",
             "It did change, but the Variables pane only refreshes on render",
         ],
         answer=1),

    dict(type="mc", points=1, source="Lab Q4",
         text="You close Positron, reopen it the next day, and R says "
              "<code>could not find function</code> when you use a tidyverse "
              "function. Which line must be run again, and why?",
         choices=[
             "<code>library(tidyverse)</code> — loading into memory is lost when the session ends; "
             "the install on disk is not",
             "<code>install.packages(\"tidyverse\")</code> — packages are deleted when Positron closes",
             "Both lines — every new session starts from a blank computer",
             "Neither line — Positron reloads all packages automatically",
             "<code>install.packages(\"tidyverse\")</code> — installing also loads the package",
             "<code>library(tidyverse)</code> — but only because the file was saved in a new folder",
         ],
         answer=0),

    # ---- Part B · Data types ---------------------------------------------
    dict(type="mc", points=1, source="Lab Q5",
         text="<code>mtcars$cyl</code> only ever takes the values 4, 6, or 8. What "
              "did <code>class(mtcars$cyl)</code> return in your lab?",
         choices=['"numeric"', '"factor"', '"character"', '"integer"', '"logical"', '"category"'],
         answer=0),

    dict(type="mc", points=1, source="Lab Q6",
         text="With its default arguments, what does <code>mean(c(1, 2, NA))</code> return?",
         choices=["<code>NA</code>", "1.5", "1", "0", "An error", "3"],
         answer=0),

    dict(type="num", points=1, source="Lab Q7",
         text="How many missing values does <code>sum(is.na(c(88, 92, NA, 75, NA, 100)))</code> report?",
         answer=2, tol=0),

    dict(type="mc", points=1, source="Lab Q7 (concept)",
         text="Why does <code>sum(is.na(x))</code> count the missing values in <code>x</code>?",
         choices=[
             "<code>is.na()</code> returns one TRUE/FALSE per value, and <code>sum()</code> "
             "treats TRUE as 1 and FALSE as 0",
             "<code>sum()</code> ignores everything except NA values",
             "<code>is.na()</code> returns the number of NAs directly; <code>sum()</code> just prints it",
             "<code>is.na()</code> removes the NAs and <code>sum()</code> counts what was removed",
             "<code>sum()</code> converts NA to 1 before adding",
             "It does not — <code>sum()</code> returns NA whenever NAs are present",
         ],
         answer=0),

    # ---- Part C · Data structures ----------------------------------------
    dict(type="ma", points=2, source="Lab Q11",
         text="In Lab Q11 you printed the same menu as a <code>data.frame</code> and as a "
              "<code>tibble</code>. Select <strong>every</strong> statement that is TRUE.",
         choices=[
             "The tibble printout shows its dimensions (e.g. <code>3 × 2</code>) at the top",
             "The tibble printout shows each column's type under the column name",
             "<code>class(menu)</code> for the tibble includes <code>\"data.frame\"</code>",
             "A tibble cannot hold a text column",
             "<code>data.frame()</code> comes from the tidyverse",
             "A tibble is a data frame with nicer printing, not a different kind of object",
         ],
         answer=[0, 1, 2, 5]),

    dict(type="mc", points=1, source="Lab Q12",
         text="In the Console you tried <code>c(\"a\", 1)</code>. What did R return?",
         choices=[
             "<code>\"a\" \"1\"</code> — a character vector; the 1 became text",
             "<code>\"a\" 1</code> — a vector holding one character and one number",
             "An error: a vector cannot mix types",
             "A list with two elements",
             "<code>NA 1</code> — the text became missing",
             "<code>1</code> — the text was dropped",
         ],
         answer=0),

    dict(type="mc", points=1, source="Lab Q13",
         text="Which pair correctly gives a <strong>data type</strong> first and a "
              "<strong>data structure</strong> second?",
         choices=[
             "numeric ; list",
             "list ; numeric",
             "tibble ; vector",
             "character ; logical",
             "vector ; data frame",
             "factor ; character",
         ],
         answer=0),

    # ---- Part D · Inspecting data & storage ------------------------------
    dict(type="num", points=1, source="Lab Q14",
         text="How many ROWS (cars) does <code>dim(mtcars)</code> report?",
         answer=32, tol=0),

    dict(type="mc", points=1, source="Lab Q14 (concept)",
         text="<code>mtcars</code> never appeared in your Variables pane even though you "
              "used it all lab. Why?",
         choices=[
             "It ships inside a package, so it is available without being created by "
             "<code>&lt;-</code> in your session",
             "Built-in datasets are too large to show in the Variables pane",
             "It is only loaded when you render, not when you run a chunk",
             "The Variables pane only shows objects made with <code>tibble()</code>",
             "It was deleted when you restarted R",
             "It is stored on disk as a CSV, not in memory",
         ],
         answer=0),

    dict(type="mc", points=1, source="Lab Q15",
         text="<code>object.size(mtcars)</code> is about 7 KB for 32 rows. A dataset with "
              "the same columns but 32 <em>million</em> rows would be roughly:",
         choices=["7 GB", "7 MB", "7 KB", "700 KB", "70 MB", "It cannot be estimated"],
         answer=0),

    # ---- Part E · AI & reproducibility -----------------------------------
    dict(type="mc", points=1, source="Lab Q16",
         text="After running the AI-generated code that grouped <code>mtcars</code> by "
              "<code>cyl</code>, which cylinder group had the HIGHEST average mpg?",
         choices=["4 cylinders", "6 cylinders", "8 cylinders", "All three were equal",
                  "4 and 6 were tied", "The code cannot tell you this"],
         answer=0),

    dict(type="mc", points=1, source="Finish: render (concept)",
         text="The lab tells you to <strong>Restart R</strong> before clicking Render. "
              "What does restarting prove?",
         choices=[
             "That everything the document needs is <em>in</em> the document, not left over "
             "from something typed in the Console",
             "That your packages are installed correctly on disk",
             "That the Variables pane is working",
             "That Quarto is using the newest version of R",
             "That the document will render faster",
             "Nothing — it is only a habit for clearing plots",
         ],
         answer=0),
]

assert len(QUESTIONS) == 15, f"Expected 15 questions, have {len(QUESTIONS)}"
for _q in QUESTIONS:
    if _q["type"] in ("mc", "ma"):
        assert len(_q["choices"]) >= 5, f"Fewer than 5 choices: {_q['text'][:60]}"

# ---------------------------------------------------------------------------
# Canvas payload builders
# ---------------------------------------------------------------------------
def build_canvas_question(q: dict, idx: int) -> dict:
    payload = {
        "question_name":   f"Q{idx}",
        "question_text":   q["text"],
        "points_possible": q["points"],
    }
    if q["type"] == "mc":
        payload["question_type"] = "multiple_choice_question"
        payload["answers"] = [
            {"answer_html": c, "answer_weight": 100 if i == q["answer"] else 0}
            for i, c in enumerate(q["choices"])
        ]
    elif q["type"] == "ma":
        correct = set(q["answer"])
        payload["question_type"] = "multiple_answers_question"
        payload["answers"] = [
            {"answer_html": c, "answer_weight": 100 if i in correct else 0}
            for i, c in enumerate(q["choices"])
        ]
    elif q["type"] == "num":
        payload["question_type"] = "numerical_question"
        payload["answers"] = [{
            "numerical_answer_type": "exact_answer",
            "answer_exact":          float(q["answer"]),
            "answer_error_margin":   float(q.get("tol", 0)),
            "answer_weight":         100,
        }]
    else:
        raise ValueError(f"Unknown question type {q['type']!r}")
    return payload


def answer_key() -> str:
    total = sum(q["points"] for q in QUESTIONS)
    lines = ["# Lab 01 Quiz — Answer Key\n",
             f"Total points: {total}  ·  {len(QUESTIONS)} questions  ·  "
             f"{ALLOWED_ATTEMPTS} attempts  ·  {TIME_LIMIT_MIN} min\n"]
    for i, q in enumerate(QUESTIONS, 1):
        lines.append(f"**Q{i}** ({q['type']}, {q['points']} pt, {q['source']}) {q['text']}")
        if q["type"] == "mc":
            lines.append(f"   Correct: {q['choices'][q['answer']]}")
        elif q["type"] == "ma":
            lines.append("   Correct: " + " | ".join(q["choices"][i] for i in q["answer"]))
        else:
            lines.append(f"   Correct: {q['answer']} (tol {q.get('tol', 0)})")
        lines.append("")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Post
# ---------------------------------------------------------------------------
def post_to_canvas(publish: bool, dry_run: bool):
    quiz_payload = {
        "title":            QUIZ_TITLE,
        "description":      QUIZ_DESCRIPTION,
        "quiz_type":        "assignment",
        "published":        publish,
        "allowed_attempts": ALLOWED_ATTEMPTS,
        "scoring_policy":   "keep_highest",
        "time_limit":       TIME_LIMIT_MIN,
        "shuffle_answers":  SHUFFLE_ANSWERS,
        "show_correct_answers": False,
    }
    total = sum(q["points"] for q in QUESTIONS)

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Creating quiz: {QUIZ_TITLE}")
    print(f"  Course          : {COURSE_ID} @ {API_URL}")
    print(f"  Questions       : {len(QUESTIONS)}  ({total} points)")
    print(f"  Allowed attempts: {ALLOWED_ATTEMPTS}")
    print(f"  Time limit      : {TIME_LIMIT_MIN} min")
    print(f"  Published       : {publish}\n")

    quiz = None
    if not dry_run:
        try:
            from canvasapi import Canvas
        except ImportError:
            sys.exit("canvasapi not installed. Run: pip install canvasapi python-dotenv")
        if not API_KEY:
            sys.exit("Missing CANVAS_API_KEY. Put it in the project-root .env file.")
        course = Canvas(API_URL, API_KEY).get_course(COURSE_ID)
        quiz = course.create_quiz(quiz_payload)
        print(f"  Quiz created -> ID {quiz.id}")

    for i, q in enumerate(QUESTIONS, 1):
        cq = build_canvas_question(q, i)
        if dry_run:
            print(f"  Q{i:02d} [{cq['question_type']}] {q['source']}  pts={cq['points_possible']}")
            for a in cq["answers"]:
                mark = "*" if a["answer_weight"] == 100 else " "
                print(f"       [{mark}] {str(a.get('answer_html', a.get('answer_exact')))[:90]}")
        else:
            quiz.create_question(question=cq)
            print(f"  Posted Q{i:02d} ({q['source']})")

    if dry_run:
        print("\n[DRY RUN] No changes made to Canvas.")
    else:
        status = "published" if publish else "draft (unpublished)"
        print(f"\nDone — '{QUIZ_TITLE}' posted as {status}.")
        print(f"   {API_URL}/courses/{COURSE_ID}/quizzes/{quiz.id}")


def main():
    ap = argparse.ArgumentParser(description="Post the Lab 01 quiz to Canvas.")
    ap.add_argument("--publish", action="store_true", help="publish immediately (default: draft)")
    ap.add_argument("--dry-run", action="store_true", help="print payloads; post nothing")
    args = ap.parse_args()

    key_path = HERE / "lab01_answer_key.md"
    key_path.write_text(answer_key())
    print(f"Wrote {key_path.name}")

    post_to_canvas(publish=args.publish, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
