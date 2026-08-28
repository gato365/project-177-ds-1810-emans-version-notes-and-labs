# Lab 02 Quiz — Answer Key

Total points: 15  ·  15 questions  ·  3 attempts  ·  120 min

**Q1** (mc, 1 pt, Lab Q1) What did <code>class(5.45 &gt; 4.75)</code> return in your lab?
   Correct: "logical"

**Q2** (mc, 1 pt, Lab Q3) In the Console you ran <code>factor(c("morning", "Morning"), levels = c("morning", "afternoon", "evening"))</code>. What happened to <code>"Morning"</code>?
   Correct: It became <code>NA</code> — silently, with no error

**Q3** (mc, 1 pt, Lab Q3 (concept)) <code>table(slot_chr)</code> and <code>table(slot_fct)</code> show the same counts in a different order. What decides the order for the factor version?
   Correct: The <code>levels</code> you gave when creating the factor

**Q4** (mc, 1 pt, Lab Q5) You built <code>price_broken &lt;- c(4.75, "5.45", 5.95)</code>. What is <code>class(price_broken)</code>, and why?
   Correct: <code>"character"</code> — a vector holds one type, so R coerced every value to text

**Q5** (mc, 1 pt, Lab Q6b) In Q6b you gave <code>price</code> only two values inside <code>tibble()</code>. What did the error message tell you?
   Correct: The sizes involved (3 vs 2) <em>and</em> which column broke (<code>price</code>)

**Q6** (num, 1 pt, Lab Q6) How many columns does <code>ncol(lattes)</code> report for your <code>lattes</code> tibble?
   Correct: 3 (tol 0)

**Q7** (mc, 1 pt, Lab Q7) What can a <strong>list</strong> do that a vector cannot?
   Correct: Hold parts of different types — even a whole tibble — without changing any of them

**Q8** (mc, 1 pt, Lab Q9) From <code>summary(airquality)</code>: which two columns contain missing values, and how many each?
   Correct: Ozone (37) and Solar.R (7)

**Q9** (mc, 1 pt, Lab Q9 (concept)) <code>airquality</code> never appeared in your Variables pane even though you used it all lab, but <code>july_temp</code> did. Why?
   Correct: <code>july_temp</code> was created in your session with <code>&lt;-</code>; <code>airquality</code> ships inside a package

**Q10** (num, 1 pt, Lab Q10) What does <code>sum(airquality$Temp &gt; 90)</code> return — how many days were above 90°F?
   Correct: 14 (tol 0)

**Q11** (mc, 1 pt, Lab Q10 (concept)) <code>mean(airquality$Ozone)</code> returns <code>NA</code>. Which line fixes it?
   Correct: <code>mean(airquality$Ozone, na.rm = TRUE)</code>

**Q12** (num, 1 pt, Lab Q12) What is <code>length(july_temp)</code> — how many July days are in <code>airquality</code>?
   Correct: 31 (tol 0)

**Q13** (mc, 1 pt, Lab Q13) Which pipe is exactly equivalent to <code>round(mean(airquality$Ozone, na.rm = TRUE), 1)</code>?
   Correct: <code>airquality$Ozone |&gt; mean(na.rm = TRUE) |&gt; round(1)</code>

**Q14** (mc, 1 pt, Lab Q15) <code>airquality</code> is 153 rows and about 5.6 KB. The same six columns for about 8.8 million rows would be roughly:
   Correct: A few hundred MB

**Q15** (mc, 1 pt, Lab Q16) After running the AI-generated code that turned <code>Month</code> into a factor with month names and counted the days, how many days did <strong>June</strong> have?
   Correct: 30
