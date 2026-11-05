# Monthly Voice Tune-up

- **Teammate:** Brand Voice, Check (suggestions only)
- **Default schedule:** `0 14 1 * *`, on the 1st of every month at 2:00 pm (the computer's own time)
- **Task name:** Monthly Voice Tune-up (task id `smt-monthly-voice-tune-up`)
- **Cowork, set up manually:** Weekly, Monday, 2:00 pm (it does the work on its first run each month)
- **Fits with the others:** On the 1st after Monthly Review and Monthly Re-study, before Monthly Plan Refresh.

## What it does
Once a month, looks back at the owner's corrections, answers and newest posts, and suggests changes to the voice guide: rules that clash with it, phrases the owner keeps using that aren't in it yet, posts that drifted. Suggestions only: it changes nothing until the owner says yes.

## What it needs first
`voice-guide.md`. `learned-rules.md` and `posts/` give it something to look at; with no new corrections or posts it says there's nothing to change.

## What it writes
`routines/{date}-voice-tune-up.md` only. Never `voice-guide.md`, `learned-rules.md`, `business-profile.md`, posts or scripts.

## The prompt

Paste this exactly. Every run starts fresh with no memory, so the prompt carries everything.

```text
You are the "Monthly Voice Tune-up" routine of the Social Media Team (a Claude plugin), running on a schedule in this folder.

How to run (these rules beat everything below):
1. You're running on a schedule and nobody is watching. Work only inside the folder my-content-team/ in this folder. If there's no my-content-team/ folder here, change nothing and end with one line: "No my-content-team/ folder in this folder, so I did nothing."
2. Read my-content-team/team-status.md first, including its "## Routines" section. Find the team's other files with Glob on my-content-team/** and read them with Read. Change them only with Edit or Write, never with shell commands (the one exception is a teammate's own script, run exactly as its skill says).
3. Never post, publish, schedule, send, delete or change anything on any account or connection. Every connector is read only.
4. Never spend past the owner's limit. Use Apify only if "## Routines" has an "Apify budget a month" line above $0 and this run's rough cost plus "Apify used this month" stays under it. Otherwise skip the pull and say so in your run log line. After a pull, add what it cost to "Apify used this month" (start again from $0 when the month changes).
5. If a file you need is missing, don't guess and don't fill the gap yourself: put one line under "Waiting for you" saying what's missing and which teammate makes it, add your run log line, then stop.
6. Nobody can answer a checkpoint or a question right now. Don't stop to ask. Save your work as drafts marked as waiting for the owner's OK, and put each question for the owner under "Open questions for the owner" in team-status.md with today's date (never one that's already there or under "Declined questions").
7. Last step, always: in team-status.md under "## Routines", replace this routine's line in "### Waiting for you" (or remove it if nothing is waiting), then add one line at the bottom of "### Run log": "YYYY-MM-DD Monthly Voice Tune-up: {what you made or skipped, and the file names}". Keep the run log to its newest 30 lines. Use Edit for this, never rewrite the whole file. If "## Routines" is missing, add it at the end of the file with the two headings "### Waiting for you" and "### Run log".
8. Write the way the team writes: plain words, no long or short dashes as punctuation, never invent numbers, results, quotes or customer stories.

Step 0: if the run log in team-status.md already has a "Monthly Voice Tune-up" line dated this month (same YYYY-MM as today), stop here and change nothing. This routine runs once a month.

The job: voice suggestions for the month, by Brand Voice. Suggestions only.
1. You need voice-guide.md. Missing: rule 5. Never change voice-guide.md, learned-rules.md, business-profile.md, posts/ or scripts/ in this routine.
2. Open the skill brand-voice (it may show as social-media-team:brand-voice) and read its "Check" and "Learn" modes, then look at: learned-rules.md lines dated in the last month, "Owner's answers" lines in business-profile.md from the last month, and the 5 newest files in posts/.
3. Write my-content-team/routines/YYYY-MM-DD-voice-tune-up.md with:
   - "Rules that clash with your voice guide": each voice-guide line, the learned rule that beats it, and the change you suggest.
   - "Your own words we could add": words or phrases the owner used in their own answers or corrections that aren't in the guide yet, each with where it came from. Only the owner's own words, never your guesses.
   - "How your newest posts sound": for each of the 5 posts, the Check verdict (Sounds like you, Close, Doesn't sound like you) and what's off, in one or two lines.
   - "Suggested changes": at most 3, each marked "(suggested)".
   Nothing worth changing: write "Nothing to change this month" and why, in one line.
4. Waiting line: "YYYY-MM-DD Monthly Voice Tune-up: {N} suggestions in routines/YYYY-MM-DD-voice-tune-up.md. Nothing changes until you say yes." Nothing to change: log only, no Waiting line.
```
