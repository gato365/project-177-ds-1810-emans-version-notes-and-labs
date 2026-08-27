# Lab 01 Quiz — Answer Key

Total points: 16  ·  15 questions  ·  3 attempts  ·  120 min

**Q1** (mc, 1 pt, Lab Q1) In Positron, which pane answers one command at a time and forgets that command when the session ends?
   Correct: Console

**Q2** (mc, 1 pt, Lab Q3 (concept)) Why did <code>wheels</code> keep its value after you changed <code>cars_counted</code> in the Console?
   Correct: Assignment stores the <em>result</em> of the calculation at the moment it runs; <code>wheels</code> is not linked to <code>cars_counted</code> afterward

**Q3** (mc, 1 pt, Lab Q4) You close Positron, reopen it the next day, and R says <code>could not find function</code> when you use a tidyverse function. Which line must be run again, and why?
   Correct: <code>library(tidyverse)</code> — loading into memory is lost when the session ends; the install on disk is not

**Q4** (mc, 1 pt, Lab Q5) <code>mtcars$cyl</code> only ever takes the values 4, 6, or 8. What did <code>class(mtcars$cyl)</code> return in your lab?
   Correct: "numeric"

**Q5** (mc, 1 pt, Lab Q6) With its default arguments, what does <code>mean(c(1, 2, NA))</code> return?
   Correct: <code>NA</code>

**Q6** (num, 1 pt, Lab Q7) How many missing values does <code>sum(is.na(c(88, 92, NA, 75, NA, 100)))</code> report?
   Correct: 2 (tol 0)

**Q7** (mc, 1 pt, Lab Q7 (concept)) Why does <code>sum(is.na(x))</code> count the missing values in <code>x</code>?
   Correct: <code>is.na()</code> returns one TRUE/FALSE per value, and <code>sum()</code> treats TRUE as 1 and FALSE as 0

**Q8** (ma, 2 pt, Lab Q11) In Lab Q11 you printed the same menu as a <code>data.frame</code> and as a <code>tibble</code>. Select <strong>every</strong> statement that is TRUE.
   Correct: The tibble printout shows its dimensions (e.g. <code>3 × 2</code>) at the top | The tibble printout shows each column's type under the column name | <code>class(menu)</code> for the tibble includes <code>"data.frame"</code> | A tibble is a data frame with nicer printing, not a different kind of object

**Q9** (mc, 1 pt, Lab Q12) In the Console you tried <code>c("a", 1)</code>. What did R return?
   Correct: <code>"a" "1"</code> — a character vector; the 1 became text

**Q10** (mc, 1 pt, Lab Q13) Which pair correctly gives a <strong>data type</strong> first and a <strong>data structure</strong> second?
   Correct: numeric ; list

**Q11** (num, 1 pt, Lab Q14) How many ROWS (cars) does <code>dim(mtcars)</code> report?
   Correct: 32 (tol 0)

**Q12** (mc, 1 pt, Lab Q14 (concept)) <code>mtcars</code> never appeared in your Variables pane even though you used it all lab. Why?
   Correct: It ships inside a package, so it is available without being created by <code>&lt;-</code> in your session

**Q13** (mc, 1 pt, Lab Q15) <code>object.size(mtcars)</code> is about 7 KB for 32 rows. A dataset with the same columns but 32 <em>million</em> rows would be roughly:
   Correct: 7 GB

**Q14** (mc, 1 pt, Lab Q16) After running the AI-generated code that grouped <code>mtcars</code> by <code>cyl</code>, which cylinder group had the HIGHEST average mpg?
   Correct: 4 cylinders

**Q15** (mc, 1 pt, Finish: render (concept)) The lab tells you to <strong>Restart R</strong> before clicking Render. What does restarting prove?
   Correct: That everything the document needs is <em>in</em> the document, not left over from something typed in the Console
