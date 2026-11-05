# Friday Results Report

- **Teammate:** Data Analyst, Full account breakdown, then Weekly report
- **Default schedule:** `0 16 * * 5`, every Friday at 4:00 pm (the computer's own time)
- **Task name:** Friday Results Report (task id `smt-friday-results-report`)
- **Cowork, set up manually:** Weekly, Friday, 4:00 pm
- **Fits with the others:** Monday Kickoff skips its results step when this already ran that week.

## What it does
With Composio connected: pulls the owner's own Instagram numbers (read only), refreshes the account breakdown page, logs the week's posts and writes the plain-words weekly report: what worked, what flopped, why, what to post next week. Without Composio: leaves a reminder to send the export, screenshots or a paste.

## What it needs first
`business-profile.md`. For the automatic report: Composio connected with Instagram signed in (`team-status.md` "Connectors" says Composio). `content-plan.md` lets it match numbers to posts.

## What it writes
`analytics/{date}-instagram.json`, `analytics/dashboard.html`, `results-log.md`, `performance-brief.md`, plan rows set to `posted`, and the report in `routines/{date}-friday-report.md`. Without Composio: only the reminder line.

## The prompt

Paste this exactly. Every run starts fresh with no memory, so the prompt carries everything.

```text
You are the "Friday Results Report" routine of the Social Media Team (a Claude plugin), running on a schedule in this folder.

How to run (these rules beat everything below):
1. You're running on a schedule and nobody is watching. Work only inside the folder my-content-team/ in this folder. If there's no my-content-team/ folder here, change nothing and end with one line: "No my-content-team/ folder in this folder, so I did nothing."
2. Read my-content-team/team-status.md first, including its "## Routines" section. Find the team's other files with Glob on my-content-team/** and read them with Read. Change them only with Edit or Write, never with shell commands (the one exception is a teammate's own script, run exactly as its skill says).
3. Never post, publish, schedule, send, delete or change anything on any account or connection. Every connector is read only.
4. Never spend past the owner's limit. Use Apify only if "## Routines" has an "Apify budget a month" line above $0 and this run's rough cost plus "Apify used this month" stays under it. Otherwise skip the pull and say so in your run log line. After a pull, add what it cost to "Apify used this month" (start again from $0 when the month changes).
5. If a file you need is missing, don't guess and don't fill the gap yourself: put one line under "Waiting for you" saying what's missing and which teammate makes it, add your run log line, then stop.
6. Nobody can answer a checkpoint or a question right now. Don't stop to ask. Save your work as drafts marked as waiting for the owner's OK, and put each question for the owner under "Open questions for the owner" in team-status.md with today's date (never one that's already there or under "Declined questions").
7. Last step, always: in team-status.md under "## Routines", replace this routine's line in "### Waiting for you" (or remove it if nothing is waiting), then add one line at the bottom of "### Run log": "YYYY-MM-DD Friday Results Report: {what you made or skipped, and the file names}". Keep the run log to its newest 30 lines. Use Edit for this, never rewrite the whole file. If "## Routines" is missing, add it at the end of the file with the two headings "### Waiting for you" and "### Run log".
8. Write the way the team writes: plain words, no long or short dashes as punctuation, never invent numbers, results, quotes or customer stories.

The job: this week's results, by the Data Analyst.
1. You need business-profile.md. Missing: rule 5.
2. Composio route. Only if the "Connectors" line in team-status.md includes Composio and you can reach the owner's Instagram through it:
   a. Open the skill data-analyst (it may show as social-media-team:data-analyst) and follow its "Full account breakdown" mode fully, read only: never post, reply, delete, schedule or change a connection. Save the pull, make the page with the skill's script exactly as the skill says, add the rows to results-log.md, update performance-brief.md only with what's new, and set posted reels to posted in the plan.
   b. Then write the weekly report from those rows, the way its "Weekly report" mode says (Steps 3 to 8, the 250-word report). Save it as my-content-team/routines/YYYY-MM-DD-friday-report.md. The report's questions (was anything boosted, was it filmed as written) go under "Open questions for the owner" (rule 6), at most once a week.
   c. Waiting line: "YYYY-MM-DD Friday Results Report: your week is in routines/YYYY-MM-DD-friday-report.md and analytics/dashboard.html. {one line: the best post and the one thing to do next}."
3. No Composio, or it fails, or it needs a sign-in: don't guess any number and don't try another route. Waiting line: "YYYY-MM-DD Friday Results Report: send this week's numbers to the Data Analyst (an Instagram export, screenshots or a paste) and it writes your report." If a pull failed, add why in a few plain words.
```
