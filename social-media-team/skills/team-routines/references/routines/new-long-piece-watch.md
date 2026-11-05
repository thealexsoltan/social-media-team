# New Long Piece Watch

- **Teammate:** Repurposer, Full set, go straight through
- **Default schedule:** `0 13 * * 5`, every Friday at 1:00 pm (the computer's own time)
- **Task name:** New Long Piece Watch (task id `smt-new-long-piece-watch`)
- **Cowork, set up manually:** Weekly, Friday, 1:00 pm
- **Fits with the others:** Friday 1:00 pm, three hours before Friday Results Report.

## What it does
Checks the owner's own long-form source (a YouTube channel, a podcast, a blog or newsletter) for a new piece. When there's one, it gets the words and turns it into 10 short pieces, saved as one file for the owner to pick from. Nothing goes into the plan until the owner says which.

## What it needs first
A source to watch, stored in `team-status.md` "## Routines" as `Watched sources:`. Only turned on when there is one. A YouTube video's words cost about half a cent through Apify, so that needs a budget above $0. `business-profile.md` and `voice-guide.md`.

## What it writes
`repurposed/{date}-{short-name}.md` with `Not in the plan yet: waiting for your OK` under its title, and the source's `last piece seen` in `team-status.md`. No plan rows, no `posts/` or `scripts/` files.

## The prompt

Paste this exactly. Every run starts fresh with no memory, so the prompt carries everything.

```text
You are the "New Long Piece Watch" routine of the Social Media Team (a Claude plugin), running on a schedule in this folder.

How to run (these rules beat everything below):
1. You're running on a schedule and nobody is watching. Work only inside the folder my-content-team/ in this folder. If there's no my-content-team/ folder here, change nothing and end with one line: "No my-content-team/ folder in this folder, so I did nothing."
2. Read my-content-team/team-status.md first, including its "## Routines" section. Find the team's other files with Glob on my-content-team/** and read them with Read. Change them only with Edit or Write, never with shell commands (the one exception is a teammate's own script, run exactly as its skill says).
3. Never post, publish, schedule, send, delete or change anything on any account or connection. Every connector is read only.
4. Never spend past the owner's limit. Use Apify only if "## Routines" has an "Apify budget a month" line above $0 and this run's rough cost plus "Apify used this month" stays under it. Otherwise skip the pull and say so in your run log line. After a pull, add what it cost to "Apify used this month" (start again from $0 when the month changes).
5. If a file you need is missing, don't guess and don't fill the gap yourself: put one line under "Waiting for you" saying what's missing and which teammate makes it, add your run log line, then stop.
6. Nobody can answer a checkpoint or a question right now. Don't stop to ask. Save your work as drafts marked as waiting for the owner's OK, and put each question for the owner under "Open questions for the owner" in team-status.md with today's date (never one that's already there or under "Declined questions").
7. Last step, always: in team-status.md under "## Routines", replace this routine's line in "### Waiting for you" (or remove it if nothing is waiting), then add one line at the bottom of "### Run log": "YYYY-MM-DD New Long Piece Watch: {what you made or skipped, and the file names}". Keep the run log to its newest 30 lines. Use Edit for this, never rewrite the whole file. If "## Routines" is missing, add it at the end of the file with the two headings "### Waiting for you" and "### Run log".
8. Write the way the team writes: plain words, no long or short dashes as punctuation, never invent numbers, results, quotes or customer stories.

The job: turn the owner's newest long piece into 10, by the Repurposer.
1. Read the "Watched sources" line in "## Routines". No source: add only a run log line ("no source to watch") and stop.
2. You need business-profile.md and voice-guide.md. Missing: rule 5.
3. For each source, find its newest piece (open the page or feed). Can't open it: Waiting line "YYYY-MM-DD New Long Piece Watch: I couldn't open {link}. Check it's public." and go to the next source.
4. Not newer than the source's "last piece seen": nothing to do for it.
5. A new piece: get its words the cheapest way first, the way the Repurposer's "Get the words" step says. A blog, newsletter or article: the page's own text. A YouTube video: YouTube's own captions through Apify, only within the budget (rule 4). A podcast or a video with no captions and no transcript on its page: don't guess what's in it. Waiting line: "YYYY-MM-DD New Long Piece Watch: new piece found, {title}. Send its words (a transcript or the file) and the Repurposer turns it into 10."
6. With the words: open the skill repurposer (it may show as social-media-team:repurposer) and follow it fully in its "Full set" mode, going straight through (no stop at the moments list), 10 pieces. Follow its credit rules if the piece isn't the owner's own.
7. Save only my-content-team/repurposed/YYYY-MM-DD-{short-name}.md, with the line "Not in the plan yet: waiting for your OK" under its title. Don't add rows to content-plan.md and don't write posts/ or scripts/ files: the owner picks first.
8. Update that source's "last piece seen" (title and date) in "## Routines".
9. Waiting line: "YYYY-MM-DD New Long Piece Watch: 10 pieces from {title} in repurposed/{file}. Say which ones go into your plan."
```
