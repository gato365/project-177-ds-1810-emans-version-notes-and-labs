#!/usr/bin/env python3
"""
Lab 02 Canvas quiz builder — STAT/DATA 1810.

Posts the Lab 02 quiz directly to Canvas through the Canvas API (canvasapi),
and writes a human-readable answer key next to this script.

The quiz gates Lab 02: some questions ask for values students produced in the
.qmd, and the rest test the concepts the lab covers (data types vs structures, coercion, factors, tibbles, inspecting with
glimpse/summary, $ and is.na(), the pipe, storage magnitudes, reproducible rendering).

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
QUIZ_TITLE = "Lab 02 Quiz — Types, Structures & Inspection"
QUIZ_DESCRIPTION = (
    "<p>Complete the Lab 02 Quarto document first. Several questions ask for "
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
    # ---- Part A · Data types ---------------------------------------------
    dict(type="mc", points=1, source="Lab Q1",
         text="What did <code>class(5.45 &gt; 4.75)</code> return in your lab?",
         choices=['"logical"', '"numeric"', '"character"', '"integer"', '"factor"', 'TRUE'],
         answer=0),

    dict(type="mc", points=1, source="Lab Q3",
         text="In the Console you ran <code>factor(c(\"morning\", \"Morning\"), levels = c(\"morning\", \"afternoon\", \"evening\"))</code>. What happened to <code>\"Morning\"</code>?",
         choices=[
             "It became <code>NA</code> — silently, with no error",
             "R gave a red error and stopped",
             "R added a fourth level, <code>Morning</code>",
             "R corrected it to <code>morning</code>",
             "It was dropped from the vector",
             "It became the first level",
         ],
         answer=0),

    dict(type="mc", points=1, source="Lab Q3 (concept)",
         text="<code>table(slot_chr)</code> and <code>table(slot_fct)</code> show the same counts in a different order. What decides the order for the factor version?",
         choices=[
             "The <code>levels</code> you gave when creating the factor",
             "Alphabetical order, same as the character version",
             "The order the values first appear in the data",
             "The counts, largest first",
             "The Variables pane setting",
             "Random — factors have no fixed order",
         ],
         answer=0),

    # ---- Part B · Data structures ----------------------------------------
    dict(type="mc", points=1, source="Lab Q5",
         text="You built <code>price_broken &lt;- c(4.75, \"5.45\", 5.95)</code>. What is <code>class(price_broken)</code>, and why?",
         choices=[
             "<code>\"character\"</code> — a vector holds one type, so R coerced every value to text",
             "<code>\"numeric\"</code> — R ignores the quotes around numbers",
             "<code>\"list\"</code> — mixed types are stored as a list",
             "An error — a vector cannot mix types",
             "<code>\"factor\"</code> — quoted values become levels",
             "<code>\"logical\"</code> — R flags the bad value",
         ],
         answer=0),

    dict(type="mc", points=1, source="Lab Q6b",
         text="In Q6b you gave <code>price</code> only two values inside <code>tibble()</code>. What did the error message tell you?",
         choices=[
             "The sizes involved (3 vs 2) <em>and</em> which column broke (<code>price</code>)",
             "Only that \"something went wrong\"",
             "That <code>price</code> must be character",
             "That the tibble package was not loaded",
             "Nothing — it ran and filled the gap with <code>NA</code>",
             "That <code>shop</code> had too many values",
         ],
         answer=0),

    dict(type="num", points=1, source="Lab Q6",
         text="How many columns does <code>ncol(lattes)</code> report for your <code>lattes</code> tibble?",
         answer=3, tol=0),

    dict(type="mc", points=1, source="Lab Q7",
         text="What can a <strong>list</strong> do that a vector cannot?",
         choices=[
             "Hold parts of different types — even a whole tibble — without changing any of them",
             "Hold more than 100 values",
             "Be printed in the Console",
             "Store numbers with decimals",
             "Be shown in the Variables pane",
             "Be built with <code>c()</code>",
         ],
         answer=0),

    # ---- Part C · Inspecting & accessing ---------------------------------
    dict(type="mc", points=1, source="Lab Q9",
         text="From <code>summary(airquality)</code>: which two columns contain missing values, and how many each?",
         choices=[
             "Ozone (37) and Solar.R (7)",
             "Ozone (7) and Solar.R (37)",
             "Temp (37) and Wind (7)",
             "Month (5) and Day (31)",
             "Ozone (37) only",
             "None — airquality has no missing values",
         ],
         answer=0),

    dict(type="mc", points=1, source="Lab Q9 (concept)",
         text="<code>airquality</code> never appeared in your Variables pane even though you used it all lab, but <code>july_temp</code> did. Why?",
         choices=[
             "<code>july_temp</code> was created in your session with <code>&lt;-</code>; <code>airquality</code> ships inside a package",
             "Built-in datasets are too large for the Variables pane",
             "<code>airquality</code> only appears after you render",
             "Vectors are shown but data frames are not",
             "<code>airquality</code> is stored on disk as a CSV",
             "The pane only refreshes when you restart R",
         ],
         answer=0),

    dict(type="num", points=1, source="Lab Q10",
         text="What does <code>sum(airquality$Temp &gt; 90)</code> return — how many days were above 90°F?",
         answer=14, tol=0),

    dict(type="mc", points=1, source="Lab Q10 (concept)",
         text="<code>mean(airquality$Ozone)</code> returns <code>NA</code>. Which line fixes it?",
         choices=[
             "<code>mean(airquality$Ozone, na.rm = TRUE)</code>",
             "<code>mean(airquality$Ozone, na = FALSE)</code>",
             "<code>mean(is.na(airquality$Ozone))</code>",
             "<code>sum(airquality$Ozone) / 153</code>",
             "<code>mean(airquality[\"Ozone\"])</code>",
             "<code>mean(airquality$Ozone, remove = NA)</code>",
         ],
         answer=0),

    dict(type="num", points=1, source="Lab Q12",
         text="What is <code>length(july_temp)</code> — how many July days are in <code>airquality</code>?",
         answer=31, tol=0),

    # ---- Part D · Pipe & storage -----------------------------------------
    dict(type="mc", points=1, source="Lab Q13",
         text="Which pipe is exactly equivalent to <code>round(mean(airquality$Ozone, na.rm = TRUE), 1)</code>?",
         choices=[
             "<code>airquality$Ozone |&gt; mean(na.rm = TRUE) |&gt; round(1)</code>",
             "<code>airquality$Ozone |&gt; round(1) |&gt; mean(na.rm = TRUE)</code>",
             "<code>airquality$Ozone |&gt; mean() |&gt; round(1, na.rm = TRUE)</code>",
             "<code>mean |&gt; airquality$Ozone |&gt; round(1)</code>",
             "<code>airquality |&gt; Ozone |&gt; mean(na.rm = TRUE) |&gt; round(1)</code>",
             "<code>airquality$Ozone |&gt; mean(TRUE) |&gt; round(1)</code>",
         ],
         answer=0),

    dict(type="mc", points=1, source="Lab Q15",
         text="<code>airquality</code> is 153 rows and about 5.6 KB. The same six columns for about 8.8 million rows would be roughly:",
         choices=["A few hundred MB", "A few hundred KB", "A few hundred GB", "About 5 MB", "About 50 GB", "It cannot be estimated"],
         answer=0),

    # ---- Part E · AI & reproducibility -----------------------------------
    dict(type="mc", points=1, source="Lab Q16",
         text="After running the AI-generated code that turned <code>Month</code> into a factor with month names and counted the days, how many days did <strong>June</strong> have?",
         choices=["30", "31", "29", "28", "153", "The code cannot tell you this"],
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
    lines = ["# Lab 02 Quiz — Answer Key\n",
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
    ap = argparse.ArgumentParser(description="Post the Lab 02 quiz to Canvas.")
    ap.add_argument("--publish", action="store_true", help="publish immediately (default: draft)")
    ap.add_argument("--dry-run", action="store_true", help="print payloads; post nothing")
    args = ap.parse_args()

    key_path = HERE / "lab02_answer_key.md"
    key_path.write_text(answer_key())
    print(f"Wrote {key_path.name}")

    post_to_canvas(publish=args.publish, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
