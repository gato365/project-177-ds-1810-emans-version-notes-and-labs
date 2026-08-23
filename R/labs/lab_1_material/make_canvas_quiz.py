#!/usr/bin/env python3
"""
Lab 01 Canvas quiz builder — STAT/DATA 1810.

Produces a Canvas-importable QTI 1.2 .zip (Canvas: Settings -> Import Course
Content -> QTI .zip) plus a human-readable answer key. The quiz gates Lab 01:
students can only answer it if they completed the .qmd, because the questions
ask for values and objects they produced in the lab.

Grading philosophy (per course website): the lab .qmd is completion/receipt;
these quiz questions are the point-bearing artifact and are auto-graded.

Run:  python3 make_canvas_quiz.py
Out:  lab01_canvas_quiz.zip   (import into Canvas)
      lab01_answer_key.md      (your reference)

No third-party packages required (standard library only).
"""

import os, zipfile, html, textwrap, hashlib

QUIZ_TITLE = "Lab 01 Quiz — Foundations"
QUIZ_DESCRIPTION = (
    "Complete the Lab 01 Quarto document first. These questions ask for values "
    "and answers you produced there. You must render your .qmd to HTML and Word "
    "before taking this quiz."
)

# ------------------------------------------------------------------ questions
# type: "mc"  -> multiple choice (one correct)
# type: "tf"  -> true/false
# type: "num" -> numeric answer (with optional tolerance)
# type: "essay" -> manually graded short answer (the AI-reflection item)
QUESTIONS = [
    dict(type="mc", points=1,
         text="In Positron, which pane answers one command at a time?",
         choices=["Source editor", "Console", "Environment", "Help"],
         answer=1),
    dict(type="mc", points=1,
         text="In Positron, which pane lists every object you have created this session?",
         choices=["Plots", "Files", "Environment", "Terminal"],
         answer=2),
    dict(type="mc", points=1,
         text="How often do you run install.packages() for a given package on one computer?",
         choices=["Every session", "Once per computer", "Every time you load it",
                  "Never — Positron does it"],
         answer=1),
    dict(type="tf", points=1,
         text="You must run library(tidyverse) each new session before its functions work.",
         answer=True),
    dict(type="mc", points=1,
         text="What is the class() of mtcars$mpg?",
         choices=['"character"', '"numeric"', '"factor"', '"logical"'],
         answer=1),
    dict(type="num", points=1,
         text="In Q7, how many missing (NA) values are in "
              "c(88, 92, NA, 75, NA, 100)?",
         answer=2, tol=0),
    dict(type="mc", points=1,
         text="What does the na.rm = TRUE argument to mean() do?",
         choices=["Rounds the result", "Removes NA values before computing",
                  "Returns NA if any value is missing", "Sorts the data first"],
         answer=1),
    dict(type="mc", points=1,
         text="Which function did you use to build a data frame from scratch in Q10?",
         choices=["c()", "list()", "tibble()", "matrix()"],
         answer=2),
    dict(type="mc", points=1,
         text="Which structure can hold different data types at once (e.g., text, a "
              "number, and a whole tibble)?",
         choices=["A vector", "A list", "A matrix", "A numeric column"],
         answer=1),
    dict(type="num", points=1,
         text="How many ROWS (cars) are in mtcars? (from glimpse/dim in Q13)",
         answer=32, tol=0),
    dict(type="num", points=1,
         text="How many COLUMNS (variables) are in mtcars?",
         answer=11, tol=0),
    dict(type="mc", points=1,
         text="What does ONE row of mtcars represent?",
         choices=["One measurement occasion", "One car model",
                  "One manufacturer", "One year"],
         answer=1),
    dict(type="tf", points=1,
         text="Dataset size matters before importing because R loads data into "
              "memory, so a file larger than available memory may not import.",
         answer=True),
    dict(type="mc", points=1,
         text="In Q15, after grouping mtcars by cyl, which cylinder group had the "
              "HIGHEST average mpg?",
         choices=["4 cylinders", "6 cylinders", "8 cylinders",
                  "They were equal"],
         answer=0),
    dict(type="essay", points=1,
         text="Paste ONE sentence you wrote in Q15 explaining what one piece of the "
              "AI-generated code does, and name one thing in that code you do not "
              "yet fully understand. (Graded for a genuine attempt, not correctness.)"),
]

# ------------------------------------------------------------------ QTI writer
def ident(seed):
    return "q" + hashlib.md5(seed.encode()).hexdigest()[:12]

def item_xml(q, idx):
    qid = ident(q["text"])
    title = f"Q{idx+1}"
    pts = q["points"]

    if q["type"] in ("mc", "tf"):
        if q["type"] == "tf":
            choices = ["True", "False"]
            correct_idx = 0 if q["answer"] is True else 1
        else:
            choices = q["choices"]
            correct_idx = q["answer"]
        resp_labels = "".join(
            f'<response_label ident="{qid}_{i}"><material><mattext texttype="text/plain">'
            f'{html.escape(c)}</mattext></material></response_label>'
            for i, c in enumerate(choices)
        )
        respconditions = (
            f'<respcondition continue="No"><conditionvar>'
            f'<varequal respident="response1">{qid}_{correct_idx}</varequal>'
            f'</conditionvar><setvar action="Set" varname="SCORE">100</setvar>'
            f'</respcondition>'
        )
        return f'''<item ident="{qid}" title="{title}">
<itemmetadata><qtimetadata>
<qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>multiple_choice_question</fieldentry></qtimetadatafield>
<qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>{pts}</fieldentry></qtimetadatafield>
</qtimetadata></itemmetadata>
<presentation><material><mattext texttype="text/html">{html.escape(q["text"])}</mattext></material>
<response_lid ident="response1" rcardinality="Single"><render_choice>{resp_labels}</render_choice></response_lid>
</presentation>
<resprocessing><outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>
{respconditions}</resprocessing>
</item>'''

    if q["type"] == "num":
        tol = q.get("tol", 0)
        lo, hi = q["answer"] - tol, q["answer"] + tol
        return f'''<item ident="{qid}" title="{title}">
<itemmetadata><qtimetadata>
<qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>numerical_question</fieldentry></qtimetadatafield>
<qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>{pts}</fieldentry></qtimetadatafield>
</qtimetadata></itemmetadata>
<presentation><material><mattext texttype="text/html">{html.escape(q["text"])}</mattext></material>
<response_str ident="response1" rcardinality="Single"><render_fib fibtype="Decimal"><response_label ident="answer1"/></render_fib></response_str>
</presentation>
<resprocessing><outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>
<respcondition continue="No"><conditionvar>
<vargte respident="response1">{lo}</vargte><varlte respident="response1">{hi}</varlte>
</conditionvar><setvar action="Set" varname="SCORE">100</setvar></respcondition>
</resprocessing>
</item>'''

    # essay (manual)
    return f'''<item ident="{qid}" title="{title}">
<itemmetadata><qtimetadata>
<qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>essay_question</fieldentry></qtimetadatafield>
<qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>{pts}</fieldentry></qtimetadatafield>
</qtimetadata></itemmetadata>
<presentation><material><mattext texttype="text/html">{html.escape(q["text"])}</mattext></material>
<response_str ident="response1" rcardinality="Single"><render_fib><response_label ident="answer1"/></render_fib></response_str>
</presentation>
<resprocessing><outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>
</resprocessing>
</item>'''

def build():
    quiz_id = ident(QUIZ_TITLE)
    items = "\n".join(item_xml(q, i) for i, q in enumerate(QUESTIONS))
    total = sum(q["points"] for q in QUESTIONS)

    assessment = f'''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2">
<assessment ident="{quiz_id}" title="{html.escape(QUIZ_TITLE)}">
<qtimetadata><qtimetadatafield>
<fieldlabel>cc_maxattempts</fieldlabel><fieldentry>3</fieldentry>
</qtimetadatafield></qtimetadata>
<section ident="root_section">
{items}
</section>
</assessment>
</questestinterop>'''

    meta = f'''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{quiz_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0">
<title>{html.escape(QUIZ_TITLE)}</title>
<description>{html.escape(QUIZ_DESCRIPTION)}</description>
<quiz_type>assignment</quiz_type>
<points_possible>{total}</points_possible>
<allowed_attempts>3</allowed_attempts>
<scoring_policy>keep_highest</scoring_policy>
</quiz>'''

    manifest = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="lab01_manifest" xmlns="http://www.imsglobal.org/xsd/imscp_v1p1">
<resources>
<resource identifier="{quiz_id}" type="imsqti_xmlv1p2">
<file href="{quiz_id}/{quiz_id}.xml"/>
<dependency identifierref="{quiz_id}_meta"/>
</resource>
<resource identifier="{quiz_id}_meta" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{quiz_id}/assessment_meta.xml">
<file href="{quiz_id}/assessment_meta.xml"/>
</resource>
</resources>
</manifest>'''

    out = "lab01_canvas_quiz.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", manifest)
        z.writestr(f"{quiz_id}/{quiz_id}.xml", assessment)
        z.writestr(f"{quiz_id}/assessment_meta.xml", meta)
    return out, total

def answer_key():
    lines = ["# Lab 01 Quiz — Answer Key\n",
             f"Total points: {sum(q['points'] for q in QUESTIONS)}  ·  "
             f"{len(QUESTIONS)} questions\n"]
    for i, q in enumerate(QUESTIONS):
        lines.append(f"**Q{i+1}** ({q['type']}, {q['points']} pt) {q['text']}")
        if q["type"] == "mc":
            lines.append(f"   Correct: {q['choices'][q['answer']]}")
        elif q["type"] == "tf":
            lines.append(f"   Correct: {q['answer']}")
        elif q["type"] == "num":
            lines.append(f"   Correct: {q['answer']} (tol {q.get('tol',0)})")
        else:
            lines.append("   Manual grade — credit a genuine attempt.")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    path, total = build()
    with open("lab01_answer_key.md", "w") as f:
        f.write(answer_key())
    print(f"Wrote {path}  ({len(QUESTIONS)} questions, {total} points)")
    print("Wrote lab01_answer_key.md")
    print("\nCanvas import: Course Settings -> Import Course Content -> "
          "QTI .zip file -> upload lab01_canvas_quiz.zip")
