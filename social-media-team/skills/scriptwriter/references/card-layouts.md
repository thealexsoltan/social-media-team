# What the Scriptwriter writes

Three kinds of file, all in `my-content-team/scripts/`, plus small changes in `content-plan.md` (section 5).

Names follow `files-layout.md`: `{date}-{short-name}.md`.
- **Date:** the day the post is planned for in `content-plan.md` (including rows you just added, section 5), or today's date if the idea isn't in any plan. Cards from one shoot all follow the same rule: never today's date for some and post dates for others. With no plan at all, all three take the shoot date.
- **Short name:** if the post is in `content-plan.md`, use the exact `Short name` from its brief. Don't make up a new one: the Copywriter and the Data Analyst reuse it, so one post can be followed from plan to results (`files-layout.md`, "One short name per post"). Only for the owner's own idea do you make one: 2 to 5 lowercase words joined with hyphens.
- If two cards would get the same name (two hooks for one post), keep the short name and add the hook type at the end: `2026-11-03-nail-trims-warning.md`.
- **Can't write files:** in a Claude Project the folder becomes part of the name: `scripts-{date}-{short-name}.md` (house rules, section 4). Wrap each file in a fence of four backticks.

---

## 1. Filming card: `scripts/{date}-{short-name}.md`

This is the layout in `script-shape.md`, with a few extra lines at the top so the Copywriter and the Data Analyst can match the card to the plan and to the results later.

```markdown
# {Short title}
Platform: {Instagram Reels | TikTok | YouTube Shorts | Facebook Reels} (also works on: {others, or "none"})
Length: about {N} seconds ({W} spoken words)
Plan tag: {REPEAT | REMIX | TEST | not from the plan}
From the plan: {post number, date and title as written in content-plan.md, e.g. "P02, 2026-11-03, Why your dog's nails click", or "owner's idea"}
Short name: {the brief's Short name, or the one you made for the owner's idea}
Status: {the post's status word in content-plan.md: scripted | filming | ready | posted. Same as the plan row. `scripted` when the idea isn't in the plan}
Talking: {on camera | voiceover only | no talking}
Format: {one format word from `formats.md`, e.g. Hands at work}
Hook type: {one hook type word from `formats.md`, e.g. Warning}
Shape: {one shape from `script-shape.md`, e.g. Customer question, or Other}
Hook came from: {your winner: "{post}" | an account you study: "{post}" | fresh, not proven yet}
Voice: {checked against voice-guide.md | no voice guide yet}

## The four hooks
- First frame: {what we see, with movement or change}
- First sound: {what we hear in the first split second}
- Text on screen: "{1 or 2 short lines}"
- Spoken: "{first sentence}" {or: none (no talking)}

## Script
| Part | Say | [SHOW] |
|---|---|---|
| Hook | "{hook line}" | {what's on screen} |
| Beat 1. Job: {beat 1's job, written for this video} | "{beat 1}" | {what's on screen} |
| Beat 2. Job: {beat 2's job} | "{beat 2}" | {what's on screen} |
| Beat 3. Job: {beat 3's job} | "{beat 3}" | {what's on screen} |
| Payoff | "{payoff line}" | {what's on screen} |
| Call to action | "{call to action}" | {what's on screen} |

## Payoff
{the line that delivers what the hook promised}

## Call to action
"{one line}" (a comment-keyword call always names the exact keyword in capitals, e.g. "Comment TRIM")

## Filming notes
- Shots to grab: {list}
- Props: {list or "none"}
- Where: {the spot}
- Can be filmed with: {other cards from the same shoot, or "on its own"}
- Watch out for: {"keep to your never-say list", plus any rules that aren't words, e.g. "no faces, no house numbers". Never quote a banned word or phrase here or in any reminder, even to forbid it: "no booking-link call", not a quoted "link in bio"}
- Sounds stiff reading it word for word? Ask for the freestyle version, or read it twice and say it your way.

## Gaps to fill
- {each `[your number]` style blank and what goes there, or "none"}

## Backup hooks
{only when the owner skipped the hook options: 2 options in the hook-options layout}
```

Rules for the header: `Format` and `Hook type` use only the words in `formats.md`, spelled the same way, so the Data Analyst can count them. If the plan's row already gives a format, use it unless the card really changed it. If nothing fits, write `Other` and a few words. Keep the header lines and their names exactly as above (the Data Analyst reads `Short name`, `From the plan`, `Format`, `Hook type` and the call to action from the card). `Status` is the line any teammate changes when the post's status changes in the plan, so the two never drift. `Shape` uses the shape names in `script-shape.md`, spelled the same way.

Rules for the table:
- The beats follow the shape's jobs in `script-shape.md`. Each beat's first row says `Beat 1. Job: ...` in the Part cell: the job written for this video in a few words, so the owner knows what that part is for.
- A beat can take 1 to 3 rows. Extra rows say `Beat 1, continued`. Every row has a [SHOW]. No empty cells.
- **No talking:** the Say column holds what appears on screen, written `Text: "..."`, or a voiceover line written `Voiceover: "..."`. The [SHOW] column still says what we see.
- Count the spoken words (or on-screen words for no talking) and work out the length at about 2.5 words a second.

---

## 2. Freestyle card (Hooks only mode): `scripts/{date}-{short-name}.md`

For owners who talk freely once the hook is set. Written only after they pick a hook.

```markdown
# {Short title} (freestyle)
Platform: {platform}
Length: aim for about {N} seconds
From the plan: {post number, date and title, or "owner's idea"}
Short name: {the brief's Short name, or the one you made}
Status: {same word as the plan row, or `scripted`}
Talking: {on camera | voiceover only | no talking}
Format: {format word from `formats.md`}
Hook type: {hook type word from `formats.md`}
Shape: {shape from `script-shape.md`}
Hook came from: {label}

## The four hooks
- First frame: {what we see}
- First sound: {what we hear}
- Text on screen: "{words}"
- Spoken: "{first sentence, said word for word}"

## Talking points (say them your way)
1. {beat 1 in a few words} (Job: {beat 1's job}) [SHOW] {what's on screen}
2. {beat 2} (Job: {beat 2's job}) [SHOW] {what's on screen}
3. {beat 3} (Job: {beat 3's job}) [SHOW] {what's on screen}

## Payoff
{what the viewer gets at the end}

## Call to action
"{one line}"
```

---

## 3. Shoot plan (One shoot, three videos): `scripts/{date}-shoot-{short-name}.md`

The date is the shoot day: the day the owner gave in chat, else the profile's "Filming day", else a day you picked, marked "(my guess)". The short name is the place, like `shoot-in-the-van`.

```markdown
# Shoot plan: {place}, {Day} {YYYY-MM-DD} {add "(my guess)" if the day isn't from the owner or the profile}
About {N} minutes of filming (rough guess)

## Cards in this shoot
1. scripts/{file} ({title}, posts {date})
2. scripts/{file} ({title}, posts {date})
3. scripts/{file} ({title}, posts {date})

## Set up once
- Spot: {where, which way to face the light}
- Phone: {vertical, height, how it's held or propped}
- Props: {everything all three cards need}
- Outfit: {note, e.g. "bring a second top so the videos don't look filmed the same day"}

## Film in this order
| Order | Card | What to film | Why now |
|---|---|---|---|
| 1 | {card} | {shot} | {reason, e.g. "the dog is clean and calm at the start"} |

**Every time estimate carries "(rough guess)"**, the total and each part ("set up: about 10 minutes (rough guess)", "card 2: about 5 minutes (rough guess)"), because we can't know how long the owner takes. Leave a part's time out rather than give it bare.

## Shots that work for more than one card
- {shot}: cards {1, 3}

## Before you pack up
- [ ] Every hook filmed at least 3 times
- [ ] Every call to action filmed at least twice
- [ ] The extra shots listed above
```

---

## 4. Quick changes after a card

Every finished card (any mode) gets this one line above the checkpoint, before the "Captions for this: /copywriter" line:

> Quick changes: shorter, freestyle version, no talking version, or a different call to action. Just say which.

Swap out the one that already applies: on a freestyle card, offer "full script" instead of "freestyle version". On a no-talking card, offer "talking version". In One shoot, three videos, add "say which card".

What each one does (then update the same file and checkpoint again):
- **Shorter:** cut to 2 beats. Keep the hook, the payoff and the call to action. Recount the words and fix the Length line.
- **Freestyle version:** turn it into a freestyle card (layout 2). The spoken hook stays word for word; the beats become talking points with their jobs.
- **No talking version:** the Say column becomes `Text: "..."` (or an optional `Voiceover: "..."`). The text on screen and the first frame carry the hook. Change the `Talking:` line, and the `Format:` line if it no longer fits (`formats.md` words only).
- **Different call to action:** use another route the profile allows, following the DM tool rule in `script-shape.md`. Still only one.

---

## 5. Updating `content-plan.md`

The Content Strategist owns this file. For rows already there we change one thing only: the **Status cell** of the posts we scripted (`files-layout.md`, "Who may write what").

- Find the post's row in its week table by post number, date or title. Change its Status cell to `scripted`, and the card's `Status:` line to the same word. A card with open blanks that are facts the owner must supply (a name, a price, a detail) is still `scripted`, with the blanks under "Gaps to fill". It stays `idea` only when a whole beat can't be written yet (SKILL.md, "Questions for the owner"). Change nothing else: no other cell, no brief, no header line except the plan's "Last updated" date.
- Status only moves forward (`idea` > `scripted` > `filming` > `ready` > `posted`). If the post is already past `scripted`, leave it and mention it.
- We never set `filming`, `ready` or `posted`. `filming` is the owner's step: they tell us when they're filming, even in One shoot, three videos.
- If the row has no Status cell, don't add one. Tell the owner in one line and leave the file as it is.
- If a single card's idea isn't in the plan (the owner's own idea), don't add it. Say in one line that the Content Strategist can add it to the plan.
- **One shoot, three videos, with videos not in the plan:** add a row for each, the way the Repurposer does. Never change, reorder or remove rows already there.
  - Where: the week each video posts in, in date order within its table (a new row goes before any later-dated row already there). Keep each week within "Videos per week we can film" (count the video rows already there) and spill the rest into later weeks; past the last week, add a `## Week N: {start} to {end}` section (Monday to Sunday) with the same columns and `Focus: added by the Scriptwriter, the Strategist can change it`.
  - Row: the plan's columns `# | Date | Day | Platform | Format | Title | Tag | Status`. The next P number after the highest in the file. A posting date after the shoot day, spread out, never two on one day. Tag `TEST` unless the owner's results show this idea won. Status `scripted`.
  - Brief: under that week's briefs, `### P{n}: {title}` with `- Short name:` (new to the plan, used for the card's file name), `- Platform and format:`, `- From: one shoot on {date}, scripts/{file}`, `- Tag:`, `- CTA route:`, `- Goes to: the owner to film, then the Copywriter`.
  - Update the header's "Mix so far", "Covers" (if you added a week) and "Last updated". Say in one line which rows you added, by their new P numbers, and to which weeks: "Added P05 to P07: P05 in the week of 2026-11-09, P06 and P07 in the week of 2026-11-16."
- **Can't write files:** follow house rules, section 4. Give the whole `content-plan.md` with only that Status cell changed. In a Project, say: "Delete the old `content-plan.md` from your Project files first, then add this one."
