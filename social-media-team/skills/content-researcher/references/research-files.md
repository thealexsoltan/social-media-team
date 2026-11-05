# The Content Researcher's files

Two files, both in `my-content-team/` (or Project files with the same names). Other teammates read them, so keep the headings and table columns exactly as written here.

| File | Read by | What they take from it |
|---|---|---|
| `competitors.md` | Content Strategist, Scriptwriter, Orchestrator | who we learn from, and each account's normal |
| `research-notes.md` | Content Strategist, Scriptwriter, Copywriter | their winners, hook patterns, what's new, the brief |

---

## competitors.md

Use the layout in `competitor-mix.md` ("competitors.md layout") exactly: the table, the optional "Your own account" section and "Gaps". Don't add, drop or rename columns. That file also has the four verdicts, including `Not checked`.

A row for an account we haven't seen yet looks like this (made up):

```markdown
| 2 | @handle | TikTok | broad | not visible yet | not visible yet | Not checked | Owner follows them, need a grid screenshot |
```

Extra rules for the table:
- **Account**: the handle exactly as the owner gave it or as you found it on a real page. Never made up.
- **Normal views**: the middle number from the grid, written with a comma (3,100). `not visible yet` until you've seen the grid.
- **Winners in last 15**: posts at 2.0 or more among the posts you used for the normal (every readable post up to 30, pinned posts and posts under 3 days old left out). If you used a number other than 15, write it like `2 of 11` or `5 of 24`.
- **Verdict**: Keep, Maybe, Skip or Not checked. If posting frequency couldn't be checked and the owner doesn't know, write `Keep (posting frequency not checked)`. An account kept only because the whole account is winning (`outlier-score.md`) gets `Keep (whole account winning)`. Keep Skip rows in the table so nobody suggests them again.
- **Why**: one short line. Add "small sample" when the normal came from fewer than 9 posts. For a whole-account Keep, give the check that passed, like `normal 80,000 is 26.7 times followers`. End it with where the numbers came from, like `(from Apify)` or `(from grid screenshot)`, since the table has no column for it.
- Keep rows numbered 1 upwards. Aim for 10 rows with the verdict Keep: 5 same, 3 broad, 2 pro.

Extra rules for "Your own account":
- Fill it only from `results-log.md` or a screenshot of the owner's own grid. Leave out boosted posts and posts under 3 days old (`outlier-score.md`).
- Until then, keep the section with `not seen` in the number cells, so the layout never changes. Write `not given` if you don't know the owner's handle.

---

## research-notes.md

The newest brief sits at the top, because that's what other teammates read first. Sections you haven't done yet stay in the file with the line `Not done yet.` so the layout never changes.

```markdown
# Research notes
Last updated: YYYY-MM-DD
Based on: {N} accounts, {N} winners studied. What's new checked YYYY-MM-DD.

## Competitor Brief

### In short
- {3 to 5 lines a busy owner reads in 20 seconds. A best topic or best format needs winners from 2 or more accounts, else "not a pattern yet"}

### Patterns to borrow
| # | Pattern (the move) | Seen in (account, score) | How you could use it |
|---|---|---|---|
| 1 | Opens on the hidden problem, close up, before any talking | @handle 4.6, @handle 3.1 | Open on the mat under the top coat, hands parting the fur |

### Hooks to test
| # | Hook pattern | From (account, score) | Your version |
|---|---|---|---|
| 1 | "If your [thing] looks fine on top, check [hidden spot]" | @handle 8.2 | "if your doodle looks fine on top, check behind the ears" |

### What not to copy
- {move + why it doesn't fit this owner, e.g. "Acted skits with 3 people: you film alone."}

### What we couldn't see
- {e.g. "@handle: only 7 posts readable, small sample." "No first sound for any winner yet."}

## Your version vs theirs
Checked: YYYY-MM-DD

### 1. Topic: {the shared topic, one line}
| | Your post | Their winner | Differs? |
|---|---|---|---|
| Post | {short name from results-log.md, or "from your grid screenshot"} | @handle (Top hooks #{N}) | |
| Score | {views} ÷ your normal {N} = {score}, or "no fair score yet ({why})" | {views} ÷ their normal {N} = {score} | |
| Spoken hook | "{first sentence}" or "not known" | "{first sentence}" or "not seen" | differs / same / can't tell |
| Text hook | | | |
| First frame | | | |
| First sound | | | |
| Format | | | |
| Length | | | |
| CTA | | | |
- Clearest difference: {one or two rows marked differs, in plain words}
- Try next time (best guess): {one change for the owner's next post on this topic}
- Couldn't compare: {rows marked can't tell, and what would fill them}

(Up to 3 pairs, clearest match first.)

## Top hooks (winners we studied)

### 1. @handle, score 8.2
- Sum: 26,300 views ÷ normal 3,200 = 8.2
- Posted: YYYY-MM-DD or "not seen"
- Link: {link or "not given"}
- Topic: {one line}
- Format: {a format from formats.md}
- Hook type: {a hook type from formats.md}
- Length: {seconds or "not seen"}
- Spoken hook: "{first sentence}" or "no talking" or "not seen"
- Text hook: "{words on screen at the start}" or "none" or "not seen"
- First frame: {what we see} (note "cover only" if you saw the grid cover, not the video)
- First sound: {voice, music, a noise} or "not seen"
- CTA: "{the ask}" or "none"
- Hook pattern: "{hook with up to 3 [blanks]}"
- Why it may have worked (best guess): {one or two lines}
- What to borrow: {the move, for this owner}
- Seen from: {grid screenshot, post screenshot, owner typed it, Apify, Deep study (with its source tags, see `deep-study.md`), Study accounts (video still, machine heard on this computer, music info; breakdown `study/{handle}/breakdowns/{code}.md`)}

(Repeat for each winner, best score first.)

## Whole account winning
Accounts where every post does well, so no single post stands out (`outlier-score.md`, whole-account check). `Not done yet.` until there's one.

### @handle
- Check: normal {N} ÷ {N} followers = {N}, and/or normal {N} ÷ group middle {N} = {N}
- Posts looked at: {N}{, small sample, check again later}
- Format: {x of y} {format from formats.md}
- Topic: {x of y} {topic}
- How they open: {x of y} {hook type from formats.md}, {first frame habit}
- Length: {x of y} {range}, or "not seen"
- CTA: {x of y} "{the ask}", or "none" or "not seen"
- What to borrow: {the habit, for this owner}
- Seen from: {Apify, grid screenshot, Deep study, ...}

## Formats that win
| Format | Winners | Accounts (scores) |
|---|---|---|
| Hands at work | 4 | @handle 4.6, @handle 3.1, @handle 2.5, @handle 2.2 |

## Hook types that win
| Hook type | Winners | Accounts (scores) |
|---|---|---|
| Before and after | 3 | @handle 4.6, @handle 3.1, @handle 2.2 |

## Topics that win
| Topic | Winners | Accounts (scores) |
|---|---|---|
| Hidden mats | 2 | @handle 8.2, @handle 2.8 |

## What's new in your niche
Checked: YYYY-MM-DD

| # | Date | What | Kind | Source | Why it's a video | Angle to try | Use by |
|---|---|---|---|---|---|---|---|
| 1 | YYYY-MM-DD | {one line} | news / season / local / question | [{site name}]({link}) or calendar | {one line for this business} | "{a hook idea}" | YYYY-MM-DD |

## Where we look for news
- {site, group, association or forum the owner named or you found useful}

## All-time hits (pinned posts)
| Account | Views | What it shows |
|---|---|---|
| @handle | 412,000 | {from the cover: one line} |
```

Rules:
- **Every pattern, hook and topic line names an account and its score**, written out in every row of every table (never "same 3", "as above" or a pointer to another row). No score, no claim.
- Scores are rounded to one decimal, with the sum shown in Top hooks.
- Format and Hook type use only the words in `formats.md`. If nothing fits, write `Other` and a few words, like `Other (acted skit, two people)`.
- "What's new" items need a real date and a real link. Season items may use `calendar` as the source. Questions people ask need the page you saw them on.
- Keep old "What's new" rows for 30 days, then drop them. Keep Top hooks until the account is dropped from `competitors.md`.
- Never write results you can't know (sales, bookings, money made) for any account.
- **Your version vs theirs**: both scores come with their sums, each against its own account's normal. Never put raw views side by side as the comparison. A row is `can't tell` when either side is `not seen`, `not known` or only guessed from a caption. Cells are copied from `results-log.md`, "Top hooks" or a screenshot, never made up. Refresh the section when the owner's log has new posts on a studied topic. Until then it reads `Not done yet.`
- **Where numbers came from**: every view count comes from `Apify`, a `grid screenshot`, a `post screenshot` or `owner typed it`. Write it in "Seen from" for each winner. Hooks read by Deep study carry its source tags (`video still`, `TikTok captions`, `Apify transcript`, `machine heard on this computer`, `music info`).

---

## A filled example (made up)

```markdown
## Top hooks (winners we studied)

### 1. @sudsandsuds.van, score 4.6
- Sum: 14,600 views ÷ normal 3,200 = 4.6
- Posted: not seen
- Link: not given
- Topic: what a matted coat looks like up close
- Format: Hands at work
- Hook type: Surprising fact
- Length: not seen
- Spoken hook: not seen
- Text hook: "this is why we shave"
- First frame: cover only: clippers sliding under a solid mat on a grey dog
- First sound: not seen
- CTA: "book link in bio"
- Hook pattern: "this is why we [thing customers hate]"
- Why it may have worked (best guess): answers the question owners argue about, and shows the proof in the first frame
- What to borrow: open on the proof, then explain. For you: the mat coming off in one piece.
- Seen from: grid screenshot, post screenshot
```
