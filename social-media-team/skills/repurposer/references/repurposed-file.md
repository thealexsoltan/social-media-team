# The Repurposer's files

## repurposed/{date}-{short-name}.md

One file per long piece. `{date}` is the day you made it (`YYYY-MM-DD`). `{short-name}` is 2 to 5 lowercase words about the piece, joined with hyphens (for example `2026-11-02-winter-pipes-live`).

In a Claude Project, which can't hold folders, the name is exactly `repurposed-{date}-{short-name}.md` (house rules section 4). The file has code blocks inside, so **in chat only** wrap the whole file in a fence of four backticks. Never write that fence into a saved file: the saved file starts with its `# Repurposed:` line and ends with its last section.

Layout:

````markdown
# Repurposed: {title of the long piece, or a short description}
Made: YYYY-MM-DD
Source: {what it was, e.g. "Facebook live transcript, about 15 minutes", "blog post 'How to drain a water heater'" or "research paper, 20 pages"}
Source link: {the link, or "pasted in chat", or the file name}
Whose: {your own | someone else's: {name, show or site} | research paper: {authors, year, title, journal or publisher}}
Words from: {pasted | the PDF | the web page | YouTube's own captions | Apify transcript | transcribed on your computer | the abstract only}
Templates: {script-templates.md, last updated YYYY-MM-DD | none yet}
Platforms: {the platforms these pieces are for}
Status: {done | approved}

## Best moments
1. **{short name}** ({kind}, {where}): "{exact words}"
2. **{short name}** ({kind}, {where}; credit: {name, show or paper, year}): "{exact words}"
3. ...

## The pieces
| # | Piece | Format | Platform | From moment | Built on | In the plan | File |
|---|---|---|---|---|---|---|---|
| 1 | Short video script, with captions | Hands at work | Instagram Reels | 3 | template 2 | P07, scripted | scripts/2026-11-04-heater-noise-warning.md (captions: posts/2026-11-04-heater-noise-warning.md) |
| 2 | Text post | Text post | Facebook | 5 | | P08, ready | posts/2026-11-05-shutoff-valve-tip.md |
| 3 | ... | | | | | | |

## 1. {title} (short video script, {platform}, built on template {N})
From moment {N}. Saved as `scripts/{file}`, captions in `posts/{file}`.
(A piece with its own file gets just these lines. Only pieces without one, like the email, or every piece when you can't write files or there's no plan, carry their text here, as below.)

```markdown
{the filming card, layout from script-shape.md}
```

```text
{the captions, one block per platform, each labelled}
```

## 2. {title} ({platform}, {kind of post})
From moment {N}.

```text
{the post, ready to paste}
```

(one section per piece, numbered in the same order as the table)

## Gaps to fill
- Piece {N}: {what's missing, e.g. "[your price] for a drain clear"}
(or "None.")

## Check before posting
- Piece {N}: {any `[check: "..."]` word from the transcript}
(or "None.")
````

Rules:
- "Format" uses the words in `formats.md`. Leave it blank for the email.
- "Built on" names the script template (`template 2`), or the shape when no template fit (`Myth shape`). Blank for posts, carousels and the email. Leave the column out when there's no `script-templates.md`.
- "Whose" and "Words from" are filled every time, so the owner (and anyone checking later) knows where every line came from. Someone else's piece or a paper: every moment from it carries its credit (`credit-rules.md`).
- "In the plan" gives the post number and status you added (see below): `P07, scripted` for a script, `P08, ready` for a text-only post, `P09, idea` for a photo or carousel waiting on a photo, `not in plan` for the email, or for every piece when there's no `content-plan.md`.
- "File" names the piece's own `scripts/` or `posts/` file (a script also names its captions' `posts/` file), or `in this file`.
- "Status" at the top is `done` once every piece is written (`draft` only while a piece is still missing). Change it to `approved` when the owner says the pieces look good.
- "Moments only" mode writes the same file with just the top block and "Best moments" (no pieces table, no pieces). A later run on the same piece adds the pieces to that file instead of starting a new one.
- "One format" mode uses the same layout with only the pieces asked for.

## Adding the pieces to content-plan.md

Only when `content-plan.md` already exists. Never create it (the Content Strategist owns it). You may add rows and their briefs, each placed in date order within its week (a new row goes before any later-dated row already there). You never change or remove anything that's already there, and the rows already there keep their order.

**Which pieces get a row.** One row per post the owner will put out:
- each short video script: Status `scripted` (the filming card exists, it still needs filming)
- each text-only post (a text post, or a carousel with plain text slides): Status `ready`
- each post that needs a photo or shot the owner hasn't said they have (photo caption, quote post on an image, a carousel on their photos): Status `idea`, with the photo it waits on in its brief's `Goes to:` line. Only the owner saying the photo exists moves it on.
- any piece that waits on an answer from the owner (a logged open question): Status `idea`, whatever its format, until the owner answers
- a caption that goes with one of the scripts: no row of its own, it's part of that script's post
- the email blurb: no row (the plan is for social posts)

**Which week.** The week the owner names. Otherwise the first week in the plan that hasn't ended yet. Add your rows to that week's table in date order (a new row goes before any later-dated row already there).

**Filming capacity.** Read "Videos per week we can film" in `business-profile.md` (or the plan's "Filming:" line). Count the video rows already in a week (any format that isn't Carousel, Photo, Text post or Story). Add script rows to that week only until it reaches that number. A week the owner just asked to lighten (in this chat or in `team-status.md`) gets no new rows of any kind; start in the week after it. The rest spill into the next week, then the one after, in date order within each week's table. If you run out of weeks, add a new `## Week N: {start} to {end}` section at the end of the file (Monday to Sunday, the week after the last one) with the same table columns, and the line `Focus: added by the Repurposer, the Strategist can change it`. Posts that need no filming don't count against video capacity, but spread them the same way: at most 2 no-filming posts a week, counting the ones already there, the rest spill into later weeks. Never pile them into one week. If "Videos per week" is "not sure" or missing, use the plan's "Filming:" line; if neither says, put the scripts in the first week and say so.

**The row.** Use the Strategist's columns exactly, in this order: `# | Date | Day | Platform | Format | Title | Tag | Status`.
- `#`: the next post number after the highest one anywhere in the file (if the last is P09, start at P10). Never reuse a number.
- Date and Day: a real date in that week and its 3-letter day (`Tue`). Pick a day with no post yet (else the one with the fewest), never two of your rows on one day, never before today.
- Platform: from the piece, main platform first.
- Format: the word from `formats.md`.
- Title: the piece's title in plain words.
- Tag: `TEST`, unless the owner's results (`results-log.md` or `performance-brief.md`) show this same idea was one of their winners, then `REPEAT`.
- Status: `scripted`, `ready` or `idea`, as above.

**The brief.** Under that week's existing briefs (before the next `## Week` heading), add a short brief for each new row:

```markdown
### P10: {title}
- Short name: {2 to 5 lowercase words joined with hyphens, not used anywhere else in the plan}
- Platform and format: {e.g. "Facebook Reels, also Instagram. Hands at work, about 25 seconds."}
- From: repurposed/{file name}, piece {N} (moment {M})
- Tag: {TEST | REPEAT}
- CTA route: {the piece's call to action, e.g. "Call: 937-555-0198" or "Book: link in bio"}
- Goes to: {the owner to film, then the Copywriter | ready to post | waiting on your photo of {what}}
```

The Scriptwriter, Copywriter and Data Analyst reuse that exact short name, so pick it once and don't change it.

**If you can't follow the plan** (no week tables, or columns you don't recognise), don't touch the file. Put the rows and briefs at the end of your reply and say: "The Content Strategist can slot these into your plan. Type /content-strategist."

**In chat**, where the plan is a Project file or was pasted in: Project files can't be edited in place, so give the whole updated `content-plan.md` in one code block, every existing line copied exactly, your rows and briefs added. Then add the matching line from house rules section 4: in a Project, "Delete the old `content-plan.md` from your Project files first, then add this one."; in plain chat, the keep-it-safe line.

**The header.** After adding rows, update the plan's header so it still matches the tables: the tag counts ("Mix so far"), "Covers" if you added a week past its end date, and "Last updated" (today's date). Change nothing else in the header.

Count your rows before you say any number. Tell the owner in one line what you added: "Added 7 posts to your content plan (P10 to P16): 2 ready to post and 2 scripts in week 1, 1 ready to post and 2 scripts in week 2, because you film 2 videos a week."

## Post and card files

Only when you can write files and you added rows. One file per row, named `{the row's date}-{the brief's short name}.md`, so the Scriptwriter, Copywriter and Data Analyst find it. Its `Status:` line always matches the row.

**A script row: `scripts/{date}-{short-name}.md`.** The filming card from `script-shape.md`, with this header under the title (the lines the team reads):

```markdown
# {Short title}
Platform: {main} (also works on: {others, or "none"})
Length: about {N} seconds ({W} spoken words)
Plan tag: {TEST | REPEAT}
From the plan: P{n}, {date}, {title}
Short name: {from the brief}
Status: scripted
Talking: {on camera | voiceover only | no talking}
Format: {a word from formats.md}
Hook type: {a word from formats.md}
Shape: {a shape from script-shape.md, or Other}
Built on: {template {N} (@{handle}, score {N}), copied from the template's "From" tag | no template fit, the {shape} shape}
Hook came from: {an account you study: "{template name}" (template {N}), filled from moment {N} | your own {source}, moment {N}}
From the source: moment {N} ({where}){; credit: {name, show or paper, year}, when it isn't the owner's}
Voice: {checked against voice-guide.md | no voice guide yet}
```

`Built on` sits right under `Shape:`, spelled the way the Scriptwriter writes it, so the whole team reads it the same way. Leave the `Built on` line out when there's no `script-templates.md`.

Then `## The four hooks`, `## Script`, `## Payoff`, `## Call to action`, `## Filming notes` and `## Gaps to fill` (or "none"), as in `script-shape.md`. No code fence around the card inside its own file.

**A post row, or the captions that go with a script: `posts/{date}-{short-name}.md`.**

````markdown
# {title}
Date to post: {the row's date}
Type: {caption pack | text post | photo post | carousel}
Platforms: {platforms}
Structure: {name from post-structures.md} (for the team only, never in the post)
Call to action: {the piece's call to action}
Offer post: {yes | no, by the definition in files-layout.md}
From: content-plan.md P{n} "{title}" (repurposed/{file}, piece {N})
Credit: {none, your own piece | {name, show or paper, year}: named in the post}
Status: {the row's status}
Captions: {written | written, waiting for {what}}
Last updated: YYYY-MM-DD

## Ready to post

### {Platform}
```text
{the post, ready to paste}
```

## Draft, needs your answer
(only for a section with an unfilled blank; leave the heading out when there are none)

## Photo to use
{photo posts only: what photo it waits on}

## Blanks to fill
{each blank and where it goes, or "None"}

## Notes
None
````

A carousel puts its slides under `## Ready to post` as `### Slide 1 (cover)` and so on, each in its own code block with a `Picture:` line, then `### Caption ({platform})`. A caption for a script uses `Type: caption pack` and the script's status.
