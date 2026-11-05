# The Content Strategist's files

The Content Strategist writes two files in `my-content-team/`: `idea-bank.md` and `content-plan.md`. Other agents read them, so keep the layouts exactly as below. Same names on every surface (folder, Project files, or copy-paste blocks).

---

## idea-bank.md

Every idea we could make, in one place: the content matrix (the owner's topics × 8 post styles) and every other idea. It grows over time. Ideas are never deleted, only marked.

```markdown
# Idea bank: {business}
Last updated: YYYY-MM-DD
Ideas: {N} in total ({n} new, {n} planned, {n} used, {n} parked)
Built from: {what fed it, e.g. "your 5 customer questions, research-notes.md (2026-10-29), no results yet"}

## Customer questions
Questions your customers ask all the time, in your words.
1. "{question}"
2. "{question}"
(Write "none given yet" if the owner hasn't shared any.)

## Content matrix
Built: YYYY-MM-DD ({T} topics × 8 post styles = {N} squares)
What you're really selling: You're not just selling {X}. You're selling {Y}.
Core message: "{one short line}"
Topics: {Topic 1}, {Topic 2}, ... (mark "(suggested)" on any we added; for grouped topics, "{Topic} (with {merged topic})")
Start with these 5: I04, I11, I19, I26, I37
Weekly rhythm: {Mon teach (How-to, List) · Wed build trust (Story, Why it works) · Fri ask for bookings (offer) ...}, {n} posts a week
Mix: Teach {x}% · Build trust {y}% · Ask for {main goal} {z}%

### Part 1 of 2: teach, inspire, explain, challenge
| Topic ↓ / Style → | How-to | Story | Why it works | Myth-buster |
|---|---|---|---|---|
| **{Topic 1}** | I01: {headline} | I02: {headline} | I03: {headline} | I04: {headline} |

### Part 2 of 2: spot, compare, look ahead, list
| Topic ↓ / Style → | Spotted | This vs that | Now vs next | List |
|---|---|---|---|---|
| **{Topic 1}** | I05: {headline} | I06: {headline} | I07: {headline} | I08: {headline} |

(Rebuilt? One line under "Built": "Rebuilt YYYY-MM-DD: {what changed}. Older ideas stay in the Ideas table.")

## Ideas
| ID | Topic | Style | Idea | Source | Tag | Best format | Status |
|---|---|---|---|---|---|---|---|
| I01 | {topic from the matrix rows} | {a Style word, see Style values} | {the headline, word for word as in the grid; for ideas outside the grid, one specific point in plain words} | {see Source values} | {REPEAT, REMIX or TEST} | {a Format word from `formats.md`, see Format values below} | {new, planned P04, used P04, parked} |

## Deeper matrix: {topic}
(Only when the owner asked to go deeper on one topic.)
Built: YYYY-MM-DD ({S} subtopics × 8 post styles = {N} squares)
Subtopics: {subtopic}: {one line on what it helps with}; ...
{the same two tables as the Content matrix, with new IDs}

## Grown ideas
### I07: {the idea}
What everyone else posts about this: {one line, the obvious take we want to go around}
Your own take: {what the owner said about this, in their words, or "not given"}

Topic check (YYYY-MM-DD, quick web search. Not facts until you check them.)
| # | Kind | What we found | Link | Check |
|---|---|---|---|---|
| F1 | People get it wrong | {one line, plain words} | {the page's full link} | check this is true for you |
| F2 | People argue about | {some say X, others say Y} | {link} | check this is true for you |
(No search possible, or nothing useful found? Write one line instead of the table: "Topic check: not done, {why}.")

| Angle | Type | One line | Hook direction | Best format |
|---|---|---|---|---|
| I07a | The mistake | {line} | {what the first 2 seconds must do} | {format} |
| I07b | The surprise | ... | ... | ... |
| I07c | The how-to | ... | ... | ... |
| I07d | The story | ... | ... | ... |
| I07e | The myth | ... | ... | ... |

## Already covered
Posted ideas, newest first, so we don't repeat ourselves by accident.
- YYYY-MM-DD: {title} (P04, idea I07)
```

**The matrix and the Ideas table.** Every square is one row in the Ideas table, with the same ID and the same headline. The grid shows the first idea in each square; extra ideas for a square (3 per square, new versions of a winner) are rows with the same Topic and Style and their own IDs. If you change a headline, change it in both places. Ideas outside the grid (offers, timely posts, old ideas from before the matrix) are rows too, with Style `none (offer)`, `none (timely)` or `none` (see Style values). How the matrix is built: `content-matrix.md`.

**Older idea banks** (no Content matrix section, no Style column): add the section and the column. Give old ideas a Style if one clearly fits (that idea can then fill its square instead of a fresh headline), else `none`. Never renumber them.

**Style values** (always these words, in this column order): `How-to`, `Story`, `Why it works`, `Myth-buster`, `Spotted`, `This vs that`, `Now vs next`, `List`. For ideas outside the grid: `none (offer)`, `none (timely)`, or `none`.

**IDs.** Ideas are `I01`, `I02` and so on, never reused. In a new matrix, number the squares row by row in column order (Topic 1 gets I01 to I08), carrying on from the last ID if the bank already had ideas. Angles add a letter: `I07a` to `I07e`. A grown angle that goes into the plan keeps its angle ID. Findings are numbered per grown idea (`F1`, `F2`) and named with the idea when used elsewhere ("F1 on I07").

**Check values** (topic check findings): `check this is true for you` (not confirmed yet), `you confirmed`, `you said no` (never used again). Only the owner's answer moves a finding off `check this is true for you`. An angle line that uses a finding names it: "(F1)". How the check works: `plan-method.md`, section 8.

**Source values** (always say where the idea came from):
- `Your winner: {post name} (score 3.1)`: a post from `results-log.md` or the "Best posts to copy from" table in `performance-brief.md`. Use the post name the way the Data Analyst writes it (for example `2026-10-14-first-bike-story`) and add the P number if it was in the plan. Copy the score from the file. Never work one out from memory.
- `Their winner: {@handle}, {few words about the post} (score 2.6)`: a post from the "Top hooks" or "Patterns to borrow" parts of `research-notes.md`. Always name the account handle as the notes write it, never "a cookie shop". Write `score not visible` if the notes don't give one.
- `Try next: {the test}`: an item from "Try next" in `performance-brief.md`. Always TEST.
- `What's new: {the thing, and where it came from}`: news, a season, a holiday, a local event.
- `Topic check: {few words} ({link}), check this is true for you`: a finding from a topic check run while building the bank (`plan-method.md`, section 8). Always TEST. When the owner confirms or rejects it, change the end to `you confirmed` or `you said no` (and park the idea if they said no).
- `Customer question {n}`: from the list above.
- `Your topics`: from the profile's topic list (or a matrix row you suggested), with no other proof yet. Most fresh matrix squares have this Source.
- `Swap of I03 ({what changed})`: a new version of an idea with one thing swapped, e.g. `Swap of I03 (older dogs instead of puppies)`. A swap tagged REPEAT or REMIX must also name the original winner post and its score, copied from the file: `Swap of I03 (older dogs) from {account} post, score 2.6`, or for the owner's own winner `Swap of I03 (older dogs) from your post 2026-10-14-first-bike-story, score 3.1`. If you can't name the winner and its score, the swap is TEST.

**Tag values:** REPEAT (a new version of the owner's own winner), REMIX (someone else's winner made the owner's own), TEST (not proven yet). A swap keeps the tag of the idea it came from only if that idea was a winner; otherwise it's TEST. A TEST idea that a new winner now proves (the winner is that idea, or a post on the same point) may be re-tagged REPEAT: change its Source to that winner post and its score, copied from the file, and change the Tag line in its brief if it's planned.

**Status values:** `new` (not in the plan), `planned P04` (in `content-plan.md` as post P04), `used P04` (posted), `parked` (the owner said no, or it doesn't fit right now).

---

## content-plan.md

What to post, when, and why. One table per week, then a short brief for every post in that week. This is the file the Scriptwriter, Copywriter and Data Analyst work from.

```markdown
# Content plan: {business}
Last updated: YYYY-MM-DD
Covers: YYYY-MM-DD to YYYY-MM-DD ({30-day plan | 30-day plan plus weekly updates})
Filming: {N} videos a week ({from business-profile.md | you told me})
Platforms: {main}, then {others}
Mix so far: {n} REPEAT, {n} REMIX, {n} TEST
Built from: {files used, e.g. "idea-bank.md, research-notes.md (2026-10-29), no results yet"}

Status steps: idea > scripted > filming > ready > posted

## Week 1: YYYY-MM-DD to YYYY-MM-DD
Focus: {one line, e.g. "fill the Tuesday and Wednesday gaps"}
Filming plan: {e.g. "film P01, P02 and P03 in one go on Monday morning". The day comes from the owner (chat or the profile's "Filming day"). "Whenever I'm on a job" becomes "film P01 and P02 on your next job where {what they need}". Only when nothing says when, add "(my guess)" after a day you picked}

| # | Date | Day | Platform | Format | Title | Tag | Status |
|---|---|---|---|---|---|---|---|
| P01 | YYYY-MM-DD | Tue | Instagram, TikTok | Talking head | {working title} | REMIX | idea |
| P02 | YYYY-MM-DD | Thu | Facebook | Photo | {working title} | TEST | idea |

### P01: {working title}
- Short name: {2 to 5 lowercase words joined with hyphens}
- Platform and format: {e.g. "Instagram Reel, also posted to TikTok. Talking head, about 30 seconds."}
- Idea: {I04, or I04a if it's a grown angle}, from the square {Topic × Style} (or "not from the matrix: offer post" / "not from the matrix: timely")
- Angle: {one line: the way into the idea. If it leans on a finding the owner hasn't confirmed, end with "(F1 on I07, not confirmed yet)"}
- Hook direction: {one line: what the first 2 seconds must do. The Scriptwriter writes the real hooks.}
- Why it should work: {the source and a plain reason. Numbers only if copied from a file. Anything about who the customers are uses the profile's own words.}
- Tag: {REPEAT, REMIX or TEST}
- CTA route: {see CTA values}
- Goes to: {Scriptwriter, then Copywriter | Copywriter}

### P02: {working title}
...

## Week 2: YYYY-MM-DD to YYYY-MM-DD
...
```

### Rules for the plan

- **Weeks run Monday to Sunday.** A 30-day plan is 4 weeks, starting the coming Monday (today, if today is Monday) unless the owner picks another start.
- **Post numbers** are `P01`, `P02` and so on across the whole file, never reused. A new week carries on from the last number.
- **Posts come from the matrix** (once the bank has one). Each brief's Idea line names its square (`Nail trims × Myth-buster`). At least 3 posts in 4 come from squares; the rest are offer or timely posts, marked "not from the matrix". Rows added by the Repurposer or Scriptwriter don't need a square.
- **One row per piece of content.** A video posted to two platforms is one row, with both platforms in the Platform cell, main platform first (for example `Instagram, TikTok`). The Data Analyst still logs one results row per platform, both under this post's short name, so each platform's numbers stay separate.
- **Status lives in the week table only.** The briefs don't repeat it, so there is one place to change it.
- **Short name** is the one name this post keeps all the way through. The Scriptwriter and Copywriter use it in their file names (`scripts/{date}-{short-name}.md`, `posts/{date}-{short-name}.md`) and the Data Analyst uses it in `results-log.md`, so one post can be followed from plan to script to caption to results. Never change a short name once a teammate has used it.
- **Titles are working titles** in plain words, so the owner knows what the post is about. They are not the final hook.
- **Past weeks stay in the file.** The Data Analyst needs them to match results to posts. Once the file holds more than 8 weeks, the oldest weeks keep their table and lose their briefs.

### Status values

Status only moves forward: idea > scripted > filming > ready > posted. The one exception: a post not yet posted whose format changes so its card or caption no longer fits goes back to `idea`, with the reason on its Status line (SKILL.md, Change the plan).

| Status | Means | Who sets it |
|---|---|---|
| idea | Planned. Nothing written yet | Content Strategist |
| scripted | Filming card written | Scriptwriter, or the Repurposer on a row it adds |
| filming | The script is done and the owner is filming it or about to | Only on the owner's word: the owner, or the Orchestrator when the owner says so. Never the Scriptwriter |
| ready | Everything needed to post exists (see the ready rule) | Copywriter (or the Repurposer, on a text-only row it adds) |
| posted | Live | Data Analyst, or you when the owner tells you it's posted |

**The ready rule.** A video is `ready` only when it's filmed **and** its caption is written. The owner tells us when a video is filmed. A caption written for a video that isn't filmed yet doesn't make it `ready`: it stays at `scripted` or `filming`. A text post is `ready` once its words are written. A photo, carousel or story that needs a photo or shot is `ready` only once its words are written **and** the owner says the photo exists.

**Who may touch the plan besides you:**
- **The Repurposer**, and the **Scriptwriter** for shoot videos that aren't in the plan yet (One shoot, three videos), may add new rows to a week's table, in date order within the week (a new row goes before any later-dated row already there), each with a short brief under that week's briefs, using the next free P numbers. Their rows start at `scripted` (a filming card exists), `ready` (a text-only post) or `idea` (a photo or carousel waiting on a photo the owner hasn't taken). Neither changes, reorders or removes rows that are already there.
- **Everyone else** (the Scriptwriter on rows already there, Copywriter, Data Analyst, and the Orchestrator for `filming`) changes **only the Status cell**, and only to the status the table above gives them. They don't add, remove or rewrite rows or briefs.

Rows they added are yours to manage from then on, like any other row. If a post needs to change (new title, new day, swapped idea), that's the Strategist's job.

### Format values

Use only the Format words in `formats.md`, the team's shared list, so results line up with the plan. What's below is only what matters for planning.

**Where each format goes:**
- Videos go to the Scriptwriter, then the Copywriter, and use filming time: Talking head, Hands at work, Voice over clips, Text on screen only, Slideshow, Screen recording.
- No-filming posts go to the Copywriter only: Carousel, Photo, Text post, Story.
- Anything the list doesn't name: `Other` with a few words, like `Other (live video)`. Plan it as a video if it needs filming time.

**Before and after** is a hook type, not a format (`formats.md`): plan it as Hands at work or Slideshow and say "before and after" in the hook direction.

If the profile says the owner is not on camera, don't use Talking head.

### CTA values

Pick from what's in `business-profile.md`. Never make up a link, number or keyword tool.
- `Book: {how, e.g. "link in bio" or "text 918-555-0142"}`
- `Call: {number from the profile}`
- `Comment {KEYWORD} for {what they get}`: **only** if the profile says the owner has a comment-to-DM tool, and only for posts on the platforms it works on. Otherwise use a booking or DM route.
- `DM: {word or "send me a message"}`
- `Soft: follow for more` or `Soft: save this for later`
