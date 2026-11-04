# Data Analyst: file and report layouts

The Data Analyst writes two files in `my-content-team/` and shows two kinds of report in chat. Other teammates read the files, so keep the layouts exact.

| What | Saved? | Read by |
|---|---|---|
| `results-log.md` | yes | Data Analyst, Content Strategist |
| `performance-brief.md` | yes | Content Strategist, Scriptwriter, Copywriter |
| `analytics/{date}-instagram.json` (a saved Composio pull, never edited) | yes | Data Analyst (`scripts/dashboard.py`) |
| `analytics/dashboard.html` (the full account breakdown page, made by the script from `assets/dashboard-template.html`) | yes | the owner |
| Weekly report | shown in chat | the owner |
| Monthly review | shown in chat | the owner |

General rules for both files:
- Dates are `YYYY-MM-DD`.
- A number you can't see is `not visible`. A number the platform doesn't give is `not given`. Never leave a cell empty and never guess.
- Numbers without commas inside tables (2800, not 2,800), so they're easy to read back. In the report, use commas (2,800).

---

## results-log.md

```markdown
# Results log: {business}
Last updated: YYYY-MM-DD
Normal right now: {N} views (the middle of {N} posts at least 3 days old, checked YYYY-MM-DD)

## Checks
One row per post per check. Newest checks at the bottom. Old rows are never changed; a later check gets a new row.

| Post | Posted | Checked | Days old | Platform | Format | Hook type | Views | Likes | Comments | Shares | Saves | Follows | Profile visits | Link taps | Normal | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-01-rusty-chain-before-after | 2026-10-01 | 2026-10-31 | 30 | Instagram | Hands at work | Before and after | 2800 | 164 | 22 | 40 | 31 | 19 | 70 | 9 | 800 | 3.5 |

## What's in each post
One row per post. Fill in what you know. Write "not known" for the rest.

| Post | Topic | Length (sec) | Spoken first line | Text on screen | First frame | First sound | Call to action | Plan tag | Where this came from | Most likely why |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-01-rusty-chain-before-after | Chain care | 41 | not known | not known | not known | not known | Text or call | not in plan | guessed from caption | the finished bike was the first frame |
| brake-squeal-warning | Brakes | 27 | "If your brakes squeal, don't wait for the weekend." | SQUEAL = BOOK IT | a brake pad worn to the metal | the squeal itself | Link in bio | REPEAT | from our card | not checked |

## Account checks
| Checked | Followers | Posts in the normal | Normal (views) | Note |
|---|---|---|---|---|
| 2026-10-31 | not given | 13 | 800 | first check, 2 posts too new |

## Working
The sums behind the latest report, replaced each time. One line each.
- 2026-10-31: rusty-chain-before-after, 2800 ÷ 800 = 3.5
- 2026-10-31: Link in bio, 38 link taps ÷ 6200 views × 1000 = 6.1 per 1000
```

Column notes:
- **Post**: if the post is in `content-plan.md` (or has a card), the exact short name from its brief ("Short name:") and nothing else, like `brake-squeal-warning`, so the post can be followed from plan to script to caption to results. The Posted column holds its date. If it isn't in the plan, `{date posted}-{2 to 5 lowercase words}`, joined with hyphens. Same name every week, so checks line up. Older rows keep the name they were logged with.
- **A video posted to two platforms** (the plan shows it as one row, with both in its Platform cell): log one row per platform per check, both under the same Post name. The Platform column tells them apart. Each row is scored against its own platform's normal, because each platform is a different account (`outlier-score.md`). When the owner posts on more than one platform, write one "Normal right now" line per platform.
- **Days old**: checked date minus posted date.
- **Format** and **Hook type**: only words from `formats.md` (how to tag: `tags.md`).
- **Link taps**: link clicks, website taps or sticker taps, whichever the platform gives. Profile visits go in their own column.
- **Normal**: the normal used for that check, so the sum can always be redone.
- **Score**: a number with one decimal, or one of `too new` (under 3 days), `no normal yet` (fewer than 9 posts old enough to count). A boosted post (ads were used) gets its score followed by the word boosted, like `3.1 boosted`, and stays out of the normal (`outlier-score.md`).
- **Plan tag**: REPEAT, REMIX or TEST if the post came from `content-plan.md`, otherwise `not in plan`.
- **Call to action**: one of `Comment keyword`, `Link in bio`, `Text`, `Call`, `Text or call` (the owner's real route: only calls is `Call`), `DM`, `Follow or save`, `None`, or `not known` (how to tag it: `tags.md`, "Call to action").
- **Where this came from**: `from our card` (taken from the post's card in `scripts/` or file in `posts/`, and the owner said they filmed it as written), `from our card, not confirmed` (same files, but the owner said no or hasn't answered), `owner told us`, `screenshot`, `export`, `Composio pull` (numbers from a saved pull in `analytics/`; the tags still come from the card or are guessed), `guessed from plan` (only the plan row, no card or post file) or `guessed from caption`. Only `from our card`, `owner told us` and `screenshot` count as known tags for a strong rule.
- **Most likely why**: one line for each winner and flop (or "did a lot worse" post), from Step 6 of the weekly report; `not checked` for the rest. A later answer adds to it rather than replacing it, unless new facts rule it out.
- **This table can be filled in later.** Unlike the Checks table, a row here may be updated when you learn more (the owner sends the first line, says they filmed it as written). An older log without the Call to action or Most likely why column: add it, and fill it from the card, the post file or the caption (`not known` if none of those say).
- If the log already has a different extra column the owner asked for, keep it.

If the owner has no normal yet, the second line reads: `Normal right now: not reliable yet ({N} posts old enough to count, we need 9)`.

---

## performance-brief.md

```markdown
# Performance brief: {business}
Last updated: YYYY-MM-DD
Based on: {N} posts from YYYY-MM-DD to YYYY-MM-DD on {platforms}. Normal: {N} views.
Goal we rank by: {goal}, measured by {the numbers used, e.g. "link taps and profile visits"}

## Rules to follow
Teammates: read these before you plan, script or write. Strong rules are safe to follow every time. Early signs are worth testing, not betting on.

1. Do {one plain line}.
   - Evidence: {counts, e.g. "3 of 3 winners opened on a before and after shot; the 2 posts that opened on a talking head scored 0.3 and 0.4"}
   - Confidence: strong | early sign
   - Since: YYYY-MM-DD
2. Don't {one plain line}.
   - Evidence: ...
   - Confidence: ...
   - Since: ...
(7 rules at most. Strong rules first.)

## Try next
- {a test worth one post, and why, e.g. "A before and after on a brake fix: brake posts have only been questions so far."}
(1 to 3 items. The Content Strategist turns these into TEST posts.)

## Your winning first lines
For the Scriptwriter: the openings that won for you. Reuse the pattern, write new words.

1. Pattern: "If your [bike part] [makes this noise], don't [what people usually do]."
   - Real line: "If your brakes squeal, don't wait for the weekend."
   - Post: brake-squeal-warning (score 2.6)
   - Used in: 2 of 2 posts with this opening were winners
   - Confidence: early sign
(Up to 5, highest score first. Or one line: "Not enough winners yet." with the reason.)

## Best posts to copy from
| Post | Score | Goal number | Why it's here |
|---|---|---|---|
| 2026-10-14-first-bike-story | 2.2 | 12 link taps | most link taps of any post |
(3 to 5 posts.)

## Retired rules
- YYYY-MM-DD: "{old rule}". Dropped because {reason, e.g. "2 later posts broke it" or "owner said"}.
```

Rules for writing the brief:
- One rule, one idea. Start with **Do** or **Don't**.
- Evidence is always counts or sums the owner can check. No "seems to", no "audiences love".
- When there's no reliable normal yet, the header says so and every rule is an early sign.
- Keep it short. Teammates read it in full before every job.
- **Your winning first lines** keeps that exact heading, `## Your winning first lines`, because the Scriptwriter looks for it. Each entry has the same five lines in the same order: Pattern, Real line, Post, Used in, Confidence. Rules for filling it: `finding-patterns.md`, "Your winning first lines". When there's nothing to list, the section still appears with one line: `Not enough winners yet.` plus why (for example "only 6 posts, we need 9 for a reliable normal" or "your 2 winners have no known first line yet").

---

## Weekly report (in chat)

```markdown
## Your week: {YYYY-MM-DD} to {YYYY-MM-DD}

{Only if the numbers end before last week: "Your numbers stop on {last date}, so last week's posts aren't in here yet."}

{The owner's own question, answered straight in one or two lines.}

**Your normal:** {N} views, the middle of your last {N} posts.
(Under 9 posts: "Your normal: not reliable yet, only {N} posts and we need 9. Your posts sit around {middle} views.")

### Winners
(Every post at 2.0 or more, by score, best first: one line each, up to 4, then "and {N} more". None: "No winners this week.")
- {post, in a few words}: {views} views, about {score} times your normal. Most likely: {reason}.

### Flops
(Every post at 0.5 or under, by score, worst first: one line each, up to 4, then "and {N} more". None: "No flops this week.")
- {post}: {views} views against your normal of {normal}. Most likely: {one line from "Most likely why", never one the card contradicts}.

(Under 9 posts the headers are "### Did a lot better than your others" and "### Did a lot worse than your others", each bullet "{views} vs about {middle}", still with the most likely reason. Never "flop" or "winner", and never a line about not using them.)

### Next week
- **Do more of:** {one item, re-counted from the log, e.g. "3 of 4 posts that opened on the dog were winners"}
- **Stop:** {one item}
- **Try:** {one item}

**Your brief:** {one line, e.g. "one new early sign: open on the dog"}.
```

**Only when the owner asked about it**, add one line after the second list:
- **Which ask brought {goal number}:** {e.g. "Link in bio brought 38 link taps, the most. Texts don't show up here, so keep a tally."}
- **Same video, different platforms:** always a small table, never a line:

| Post | Platform | Views | Score against its own normal |
|---|---|---|---|
| Orange roots | Instagram | 4,100 | 2.3 (winner) |
| Orange roots | TikTok | 900 | no normal yet (6 posts, we need 9) |

Never compare raw views between platforms as the result: the score column is the comparison.

The "Which ask" answer may be the report's one small table instead of a line: Call to action, Posts, Winners (x of y), Views, {goal number}, Per 1,000 views. Example row: `Link in bio | 4 | 2 of 4 | 9,800 | 38 link taps | 3.9`.

**Word budget**, so the parts can't pass 250:

| Part | Words at most |
|---|---|
| Header, note and normal | 30 |
| Straight answer | 25 |
| First list (all winners, up to 4 lines, then "and N more") | 60 |
| Second list (all flops, up to 4 lines, then "and N more") | 60 |
| Next week | 35 |
| Your brief | 15 |
| Which ask or Same video, only if asked (a table's words count) | 25 |

**Count before you send:** the words from the header to "Your brief", 250 at most (headings don't count). Over? Cut and count again. The whole message (report, questions, saved-file list with file names only, check-in) stays under about 300 words.

One sum at most in chat, `X ÷ Y = Z`, for the post that matters most. Every other sum, the per 1,000 working and the ranked list live in `results-log.md` (`## Working`) and `performance-brief.md`. If you need the owner's help (a first frame, the first line they said, how many bookings came in), ask at most 2 short questions after the report, before the checkpoint, and log each in "Open questions for the owner" in `team-status.md` with today's date. "Was anything boosted?" and "Did you film these as written?" are asked at most once per week of numbers, never for posts already answered.

---

## Monthly review (in chat)

```markdown
## Your month: {YYYY-MM-DD} to {YYYY-MM-DD}

### Week by week
| Week of | Posts | Normal | Winners | Flops | {goal number} |
|---|---|---|---|---|---|

### What kind of post works
| Hook type | Posts | Winners (x of y) | Views (middle) | Middle score |
|---|---|---|---|---|

| Format | Posts | Winners (x of y) | Views (middle) | Middle score |
|---|---|---|---|---|

### Topics
(Count only from the Topic column in `results-log.md`.)
- Hits: ...
- Flops: ...
- Not tested yet: ...
- Posted a lot, rarely wins: {topic}, {x} of {y} posts were winners
- Posted rarely, mostly wins: {topic}, {x} of {y} posts were winners {add "too few to judge" if under 3 posts}
(Write "none this month" for a line with nothing in it.)

### Which ask brought {goal number}
| Call to action | Posts | Winners (x of y) | Views | {goal number} | Per 1,000 views |
|---|---|---|---|---|---|
(Across every scored post in the log. "Brought the most" only for the highest total.)

### Same video, different platforms
| Post | Platform | Views | Score against its own normal |
|---|---|---|---|
(Posts this month that went out on 2 or more platforms. Leave it out if there were none.)

### Best and worst of the month
- Best: {post}, {views} ÷ {normal} = {score}, {goal number}
- Worst: {post}, {views} ÷ {normal} = {score}

### Your rules, checked
| Rule | Before | Now | Why |
|---|---|---|---|
| Do show the finished bike first | early sign | strong | 3 of 3 winners, 3 different weeks |

### Next month
- **Do more of:** ... (each line re-counted from the log, with its count)
- **Stop:** ...
- **Try:** ...
```

Small samples: if a hook type or format has only 1 or 2 posts, write the count and say "too few to judge".
