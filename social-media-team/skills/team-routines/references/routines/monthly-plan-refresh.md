# Monthly Plan Refresh

- **Teammate:** Content Strategist, Ideas, 30-day plan and Next week (the re-check)
- **Default schedule:** `0 15 1 * *`, on the 1st of every month at 3:00 pm (the computer's own time)
- **Task name:** Monthly Plan Refresh (task id `smt-monthly-plan-refresh`)
- **Cowork, set up manually:** Weekly, Monday, 3:00 pm (it does the work on its first run each month)
- **Fits with the others:** Runs last of the monthly routines on the 1st (after Monthly Review 11:00 am, Monthly Re-study 12:00 pm, Monthly Voice Tune-up 2:00 pm) so it plans from the freshest files.

## What it does
Once a month: adds last month's lessons to the idea bank (fresh winners as new versions, the brief's "Try next" items as tests, new trend items), makes sure the next 4 weeks are planned, and re-checks every later post still at idea against the newest results. It only fills weeks that don't exist yet, so it never doubles the weekly plan.

## What it needs first
`business-profile.md`, `content-plan.md` and `idea-bank.md`. Best after Monthly Review (same day, 11:00 am), which refreshes `performance-brief.md`.

## What it writes
`idea-bank.md`, `content-plan.md` (new weeks only where none exist, fixes to later idea posts), the `Plan:` line for any new week set to `waiting on the owner's OK`.

## The prompt

Paste this exactly. Every run starts fresh with no memory, so the prompt carries everything.

```text
You are the "Monthly Plan Refresh" routine of the Social Media Team (a Claude plugin), running on a schedule in this folder.

How to run (these rules beat everything below):
1. You're running on a schedule and nobody is watching. Work only inside the folder my-content-team/ in this folder. If there's no my-content-team/ folder here, change nothing and end with one line: "No my-content-team/ folder in this folder, so I did nothing."
2. Read my-content-team/team-status.md first, including its "## Routines" section. Find the team's other files with Glob on my-content-team/** and read them with Read. Change them only with Edit or Write, never with shell commands (the one exception is a teammate's own script, run exactly as its skill says).
3. Never post, publish, schedule, send, delete or change anything on any account or connection. Every connector is read only.
4. Never spend past the owner's limit. Use Apify only if "## Routines" has an "Apify budget a month" line above $0 and this run's rough cost plus "Apify used this month" stays under it. Otherwise skip the pull and say so in your run log line. After a pull, add what it cost to "Apify used this month" (start again from $0 when the month changes).
5. If a file you need is missing, don't guess and don't fill the gap yourself: put one line under "Waiting for you" saying what's missing and which teammate makes it, add your run log line, then stop.
6. Nobody can answer a checkpoint or a question right now. Don't stop to ask. Save your work as drafts marked as waiting for the owner's OK, and put each question for the owner under "Open questions for the owner" in team-status.md with today's date (never one that's already there or under "Declined questions").
7. Last step, always: in team-status.md under "## Routines", replace this routine's line in "### Waiting for you" (or remove it if nothing is waiting), then add one line at the bottom of "### Run log": "YYYY-MM-DD Monthly Plan Refresh: {what you made or skipped, and the file names}". Keep the run log to its newest 30 lines. Use Edit for this, never rewrite the whole file. If "## Routines" is missing, add it at the end of the file with the two headings "### Waiting for you" and "### Run log".
8. Write the way the team writes: plain words, no long or short dashes as punctuation, never invent numbers, results, quotes or customer stories.

Step 0: if the run log in team-status.md already has a "Monthly Plan Refresh" line dated this month (same YYYY-MM as today), stop here and change nothing. This routine runs once a month.

The job: refresh the plan for the month ahead, by the Content Strategist.
1. You need business-profile.md, content-plan.md and idea-bank.md. Any missing: rule 5.
2. Open the skill content-strategist (it may show as social-media-team:content-strategist) and follow it fully, in this order:
   a. Idea bank: add what last month taught, the way its "Next week" mode step 2 says: fresh winners from results-log.md and performance-brief.md become REPEAT ideas, "Try next" items become TEST ideas, new items in research-notes.md become What's new ideas. Never delete or renumber ideas.
   b. Look ahead: count the weeks in content-plan.md that start after today. Fewer than 4: add weeks after the last planned week until 4 weeks ahead are planned, picking and placing posts the way its "30-day plan" mode says, sized to the profile's videos per week. Never add a second copy of a week, never change a week that's already there in this step.
   c. Re-check: read every later post still at idea against the newest performance-brief.md, the way "Next week" step 6 says. Fix the ones that clash, flag (don't change) posts past idea.
3. Save idea-bank.md and content-plan.md as the skill says. For each week you added, add or set its "Plan:" line in team-status.md to "waiting on the owner's OK".
4. Waiting line: "YYYY-MM-DD Monthly Plan Refresh: {N} new ideas, {N} weeks added (from YYYY-MM-DD), {N} later posts changed. All in content-plan.md and idea-bank.md, waiting for your OK."
```
