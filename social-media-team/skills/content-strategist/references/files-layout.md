<!-- Copied from shared/files-layout.md by scripts/sync-shared.mjs. Edit the shared file, not this copy. -->
# The team's files

Every agent reads and writes these files. Same names and layout on every surface, so work moves between chat, Cowork and Claude Code.

All files live in `my-content-team/` (or as Project files with the same names).

| File | Written by | Read by |
|---|---|---|
| `business-profile.md` | Brand Voice (first run) | everyone |
| `voice-guide.md` | Brand Voice | Scriptwriter, Copywriter, Repurposer, Strategist |
| `style-guide.md` (how winning posts in the niche are built, the full guide) | Brand Voice (Mixed and path B) | Scriptwriter, Copywriter, Repurposer, Strategist |
| `first-drafts.md` (9 drafts that test the guide) | Brand Voice | the owner, Scriptwriter, Copywriter |
| `learned-rules.md` | any agent, when the owner corrects something | everyone who writes |
| `competitors.md` | Content Researcher | Strategist, Scriptwriter |
| `research-notes.md` | Content Researcher | Strategist, Scriptwriter, Copywriter |
| `study/` (a full reel study: numbers, words, pictures, breakdowns, playbook; see "study/ folder" below) | Content Researcher (Study accounts) | Brand Voice, Strategist, Scriptwriter, Copywriter |
| `script-templates.md` (fill-in-the-blank scripts from winning reels) | Content Researcher (Study accounts) | Scriptwriter, Copywriter, Repurposer |
| `idea-bank.md` (the content matrix: your topics × 8 post styles, one idea per square, plus every other idea) | Content Strategist | Strategist, Orchestrator |
| `content-plan.md` | Content Strategist | Scriptwriter, Copywriter, Data Analyst |
| `scripts/{date}-{short-name}.md` | Scriptwriter (and the Repurposer, for rows it adds) | Copywriter, Data Analyst |
| `scripts/{date}-shoot-{short-name}.md` (a plan for filming several videos in one go) | Scriptwriter | the owner |
| `posts/{date}-{short-name}.md` | Copywriter (and the Repurposer, for rows it adds) | the owner, Data Analyst |
| `repurposed/{date}-{short-name}.md` | Repurposer | the owner |
| `results-log.md` | Data Analyst | Data Analyst, Strategist |
| `performance-brief.md` | Data Analyst | Strategist, Scriptwriter, Copywriter |
| `analytics/{date}-instagram.json` (a saved Composio pull, never edited) and `analytics/dashboard.html` (the full account breakdown page; see "analytics/ folder" below) | Data Analyst (Full account breakdown) | the owner, Data Analyst |
| `team-status.md` | Orchestrator (front door), plus every teammate for the lines its work changes, plus Team Routines and every routine run for its `## Routines` section | everyone |
| `routines/{date}-{routine}.md` (what a routine made that would otherwise only be said in chat: the Friday report, the monthly review, voice suggestions, the Monday Kickoff summary) | the routine runs (Team Routines sets them up) | the owner, Orchestrator |

**"This week" and "next week":** if today is Monday, "this week" starts today. Otherwise "next week" is the coming Monday to Sunday. **First setup:** week 1 of the first plan starts on the next filming day after its scripts exist, never "today".

Dates are written `YYYY-MM-DD`. Short names are 2 to 5 lowercase words joined with hyphens.

**One short name per post.** Each post in `content-plan.md` gets a short name in its brief. The Scriptwriter, Copywriter and Data Analyst reuse that exact short name in their file names and logs, so one post can be followed from plan to script to caption to results.

**When a post's date changes,** whoever changes it renames its `scripts/` and `posts/` files to the new date with one plain `mv my-content-team/old my-content-team/new` per file, never with `cd`, `&&` or `;` (house rules section 4, "Tools"), so the name never lies. In chat there are no files to rename.

**Offer post** (the team's only definition; every teammate counts selling posts this way): an offer post names a price, a deadline, open spots or a discount, or its main message is a push to book. A helpful post that just ends with the booking line is not an offer post.

**Who may write what, outside their own files:**
- `business-profile.md`: Brand Voice, or any teammate when the owner answers the 6 quick questions, states a profile fact (on camera, filming day, video length, a new offer) or answers a question (add it to "Owner's answers").
- `team-status.md`: any teammate, only the lines its own work changed (house rules section 4).
- `learned-rules.md`: any teammate, one new line per correction.
- `posts/` and `scripts/`: Brand Voice may swap a newly banned word or phrase in unposted files, only after the owner says yes (its Learn mode). Nothing else.
- `content-plan.md`: the Strategist owns the rows. Others change **only the Status cell** of the posts they finish (and the plan's "Last updated" line): Scriptwriter > `scripted`, Copywriter > `ready` (see the status steps below), Data Analyst > `posted` (when it sees the post in the numbers, or when the owner says it's posted). Whoever changes a post's status also changes the `Status:` line in that post's file in `posts/` and its card in `scripts/`, so they never drift. The Repurposer (for its pieces) and the Scriptwriter (for shoot videos that aren't in the plan yet) may add new rows to a week's table, in date order within the week (a new row goes before any later-dated row already there); they never change or remove rows. Whoever adds rows also updates the plan's header counts and "Last updated" line, and keeps each week within the owner's filming capacity (spill extra videos into later weeks).

**Status steps** (only ever move forward, with one exception below): `idea` > `scripted` > `filming` > `ready` > `posted`.
- **The one exception:** when a post's format changes (a video becomes a photo or a text post) and its old script or caption no longer applies, a post that isn't posted goes back to `idea`, in the plan and in its files. Its `Status:` line says why: `Status: idea (was scripted, changed from video to photo on YYYY-MM-DD)`.
- `filming`: the script is done and the owner is filming it or about to.
- `ready`: everything needed to post exists. For a video that means it's filmed **and** the caption is written. The owner tells us when a video is filmed. Captions written for a video that isn't filmed yet don't make it `ready`. A post with an unfilled `[blank]` isn't `ready` either: it waits for the owner's answer. A photo, carousel or story post is `ready` only once the owner says the photo exists ("I have a photo", "I took it", or they attach it); an idea for a photo ("one can be a pic of the gunk") doesn't count, so it stays `idea` and you ask in one line. A text post, or a quote card or carousel of plain text on a plain background, is `ready` as soon as it's written.

**Each teammate's own layouts** live in its skill's `references/` folder (for example the Strategist's `strategist-files.md`). The layouts below are the ones every teammate shares.

---

## business-profile.md

The 6 quick questions (ask all in one message when the file is missing):

1. What's the business called, and what do you sell?
2. Who buys it? (Describe your best customer in a sentence or two.)
3. Where are you? (A town or area if you serve locals, or "online".)
4. Which platforms do you post on, or want to? (Instagram, TikTok, YouTube Shorts, Facebook, LinkedIn)
5. What should your posts get you, and how do people book or buy? (Bookings, sales, leads or followers. And the route: a link, a phone number, a DM, "link in bio". Is the link in your bio on every platform?)
6. Anything we should know? (Do you show your face on camera? How many videos a week can you film, and on which day? Do you have a tool that sends a DM when someone comments a word? Words or topics to never use?)

Layout:

```markdown
# Business profile
Last updated: YYYY-MM-DD

## The basics
- Business: {name}
- What we sell: {one or two lines}
- Price range: {only if the owner said it, else "not given"}
- Where: {town/area or "online"}

## Best customer
{2 to 4 lines in plain words: who they are, what they want, what bugs them}

## Goal for posting
- Main goal: {bookings | sales | leads | followers | other}
- Where people go to buy or book: {link, phone, DM, "link in bio", or "not given"}
- Link in bio on: {platforms, or "not given"}

## Platforms
- Main: {platform}
- Also: {platforms or "none yet"}

## How we make content
- On camera: {yes | no | sometimes}
- Videos per week we can film: {number or "not sure"}
- Filming day: {a day, "whenever I'm on a job" (or the owner's words), or "not given"}
- Comment-to-DM tool: {yes, name it, and which platforms it works on | no}

## Topics we post about
1. {topic}
2. {topic}
(5 to 7 topics. They become the rows of the Content Strategist's content matrix. If the owner gave fewer, suggest the rest and mark them "(suggested)".)

## Never say or show
- {anything the owner ruled out}

## Owner's answers
Answers the owner gave to our questions, in their words. Read before leaving a `[blank]`; add a line whenever they answer one.
- YYYY-MM-DD: {question in a few words}: "{their answer}"
```

---

## voice-guide.md

```markdown
# Voice guide: {business}
Last updated: YYYY-MM-DD
Built from: {what samples, e.g. "4 Instagram captions + 1 voice note", or "9 winning posts from 3 accounts + 5 answers"}
Path: {A, your own best posts | Mixed, your words + winners' post shapes | B, winners in your niche + your answers} ({the reach sum, e.g. "normal 7,500 ÷ 300,000 followers = 0.03"}, or "just starting")

## In one line
{e.g. "A friendly local who jokes a lot but knows dogs inside out."}

## Written voice (captions, posts, emails)
- Who's talking: {I | we}
- Sentence length: {short | mixed | long}, about {N} words on average
- Reading level: {very simple | simple | a bit technical}
- How posts usually start: {pattern + a real example from the samples}
- How posts usually end: {pattern + a real example}
- Emoji: {none | a few | lots}, favourites: {list or "none"}
- Punctuation habits: {e.g. "lots of exclamation marks", "no full stops at the end"}
- Humour: {none | dry | playful | puns}
- How they sell: {soft | direct | story first}

## Spoken voice (video scripts)
- Energy: {calm | warm | high energy}
- How they open a video: {pattern}
- Words and phrases they say a lot: {list}
- How they'd explain something to a friend: {one real or close example}

## Words we use
{list, taken from the samples}

## Words we never use
{the owner's own bans, word for word}
{then up to 5 extra words that clearly don't fit their voice, each marked "(suggested)" so the owner can delete any they're fine with}

## Sounds like us / doesn't sound like us
| Sounds like us | Doesn't |
|---|---|
| "{line}" | "{line}" |
(3 pairs)

## How our posts are built
{Mixed and path B only. Path A: leave this section out, or fill it from the owner's own best posts if you studied them.}
{5 to 7 lines: the top post types, the opener that wins most, how they end, length. Each with "x of y posts".}
Full guide: `style-guide.md`. Shapes only. Never a winner's own sentences, stories, names or numbers.

## What we stand for
{Only if the owner answered the deeper questions. Their words, never invented: who they are, what their customer worries about and wants, what they believe that others don't, the before and after, their story, how posts should feel and what's off limits. Otherwise: "not asked yet".}

## Test lines
1. {a short caption opener in this voice}
2. {a video opener in this voice}
3. {a call to action in this voice}
```

---

## style-guide.md

The full guide to how winning posts in the owner's niche are built (Brand Voice, Layer 2). Shapes only: never a winner's own sentences, stories, names or numbers.

```markdown
# Style guide: {business}
Last updated: YYYY-MM-DD
Built from: {N} winning posts from {accounts, with each account's normal}, plus {N} of the owner's own winners

## In one line
{what winning posts in this niche have in common}

## Post types that win
### {Type name, in plain words}
- Seen in: {x of y posts, accounts}
- How it's built: {step by step, opener to ending}
- Why it works: {best guess}
- The psychology: {the feeling and the pattern behind it}
- What it needs from you: {facts, a story, a belief, a result}
- The shape: {the moves in our words, with [blanks]}
- Points at: {who a blame or contrast may and may not point at, or "nobody"}
{2 to 5 types}

## Openers that win
{patterns with "x of y posts"}

## How the middle holds attention
{patterns with "x of y posts"}

## How they end
{patterns and calls to action, as moves, with "x of y posts"}

## Length, pacing and what's on screen
{length, lines, cuts, on-screen text, first frame, where known; "not seen" where not}

## Psychology across all of them
{the patterns that repeat}

## What winning posts never do
{list}

## Seen once only
{patterns from one post: treat as tests, or "none"}

## What we need from you to write these
{a checklist; tick what's already in the profile or "What we stand for"}
```

---

## first-drafts.md

```markdown
# First drafts
Made: YYYY-MM-DD, by Brand Voice, to test the voice and style guides
First drafts to try. The Scriptwriter and Copywriter finish the ones you like.

## {Post type 1}
1. {draft}
2. {draft}
3. {draft}
{same for post types 2 and 3}
```

---

## learned-rules.md

Every time the owner fixes a draft or states a style preference ("don't say X", "too salesy", "too long", "we never call them clients"), add one line the same turn. Edit requests count too, unless the owner says "just this once". Never delete a line unless the owner asks. Only the owner's own style rules go here, never team process rules.

```markdown
# Learned rules
The owner's own corrections. These beat the voice guide.

- YYYY-MM-DD: {the rule, in one line}. Example: "{before}" became "{after}". (Only add the example when both the before and the after are the owner's own words or a draft from this chat.)
```

---

## team-status.md

When you create it, fill the Setup lines only from files that exist (Glob first), never a guess, and leave out the instruction lines in brackets below: they're for us, not for the file.

```markdown
# Team status
Last updated: YYYY-MM-DD

## Setup
- Business profile: {done | not yet}
- Voice guide: {done | not yet | waiting for winners (path B)}
- Competitors and research: {done | not yet}
- First 30-day plan: {done | not yet}

## This week ({that week's Monday, YYYY-MM-DD})
(Replace this section and "Next week" each week, with the new Monday date. Never add a second copy.)
- Results read: {done | not yet | skipped | first week, no results yet}
- Plan: {done | waiting on the owner's OK} (change it to done the turn the owner approves: house rules section 5, "When the owner answers a checkpoint")
- Scripts: {N of M}
- Posts: {N written} of {M}, {N ready to post}

## Next week ({that week's Monday, YYYY-MM-DD})
- Plan: {done | not yet}

## Open questions for the owner
Every question any teammate asks the owner, with the date it was asked. Questions for later are asked all in one message at the end of a step, never one at a time, and never one already asked this week (a question the next step needs is asked in chat straight away, with its options). When one is answered, move the answer to "Owner's answers" in `business-profile.md` and delete the line here. If the owner's very next reply doesn't answer it, move it to "Declined questions" that same turn. When a post is posted, delete the questions about its blanks.
- {question} (needed for {post number}), asked YYYY-MM-DD

## Declined questions
The owner skipped it, said no, or didn't answer. Nobody asks again before the date (weekly opener included) unless they bring it up.
- {question}: declined YYYY-MM-DD, ask again after YYYY-MM-DD

## Where we work
- Surface: {chat | cowork | code}
- Connectors: {none | Apify | Composio | Apify and Composio}

## Routines
- Where they run: {Desktop app | Cowork}, in the folder that holds my-content-team/
- On: {each routine that's on, with its time in plain words, e.g. "Monday Content Plan (Mondays 7:00 am)"}
- Paused: {routine names, or "none"}
- Filming Prep: the evening before {filming days, e.g. "Wednesday and Sunday"}
- Apify budget a month: {$N, or "none" (routines never pull)}
- Apify used this month: {$N} ({YYYY-MM})
- Watched sources: {link} (last piece seen: "{title}", YYYY-MM-DD) | none
- Re-study: {N} reels a month from {@handles}

### Waiting for you
- YYYY-MM-DD {routine name}: {what's waiting and the file}

### Run log
- YYYY-MM-DD {routine name}: {what it did or skipped}
```

**The `## Routines` section** is only there once the owner has routines (Team Routines writes it; a routine run adds it if it's missing). Leave out the lines a routine doesn't need.
- **The lines above "Waiting for you"** (what's on, budget, sources) are changed only by Team Routines, after the owner's yes. A routine run changes only "Apify used this month" and a source's "last piece seen".
- **Waiting for you:** one line per routine, replaced by that routine's next run. Every teammate reads it at the start of a job and tells the owner what's waiting (house rules section 3). When the owner says OK to it, changes it or says skip, the teammate handling it deletes that line.
- **Run log:** one line per run, newest at the bottom, the newest 30 lines only. Only routine runs write here.
- **Drafts a routine wrote** wait for the owner's OK like any checkpoint: post files carry `Captions: waiting for your OK`, `team-status.md` lines say `waiting on the owner's OK`, a repurposed file says `Not in the plan yet: waiting for your OK`. The owner's yes moves them on (house rules section 5).

---

## CLAUDE.md (the folder note, Cowork and Claude Code only)

Lives in the working folder, next to `my-content-team/` (not inside it). Claude reads it at the start of every chat in that folder, so plain requests still reach the team. Written by Team Setup, or by the Orchestrator if it's missing or out of date (no "Always open the matching skill" line: replace the old note with this one). If the owner already has a `CLAUDE.md`, add this at the end instead of replacing it.

```markdown
## Social Media Team
This folder belongs to the Social Media Team. Its files are in `my-content-team/`.
- For any request about posts, plans, scripts, captions, numbers or corrections, use the matching social-media-team skill (orchestrator if unsure), and read `my-content-team/` first.
- Always open the matching skill before changing anything in `my-content-team/`, even a one-word edit.
- Save any correction or preference the same turn: wording to `my-content-team/learned-rules.md`, facts to `my-content-team/business-profile.md`. Say in one line where it went.
- Treat "shorter", "less salesy", "too long", "not like me" as standing preferences: save the line, say where, and tell the owner they can say "just this once" to undo it. Never cut the owner's own phrases quoted in the voice guide.
- Use Read, Glob, Grep, Write and Edit on these files, with paths relative to this folder (`my-content-team/...`), never shell commands. Exceptions: one plain `mv my-content-team/old my-content-team/new` per file to move or rename it, never with `cd`, `&&` or `;`; the Content Researcher's study script, which writes only into `my-content-team/study/`; and the Data Analyst's dashboard script, which writes only `my-content-team/analytics/dashboard.html`.
```

---

## study/ folder

Made by the Content Researcher's **Study accounts** (Claude Code or Cowork). The study script writes most of it; it's the only tool that writes inside `my-content-team/`, and only here. Other teammates read these files and never change them.

```
my-content-team/study/
  dashboard.html              every account and post in one page (open it in a browser)
  playbook.md                 what's working across the accounts, counted "x of y reels"
  {handle}/
    stats.md                  the account's numbers (made by the script, never edit by hand)
    transcripts/{code}.txt    what's said, with times (machine heard); .json has the detail
    frames/{code}/            hook.jpg (first 3 seconds), seconds-1.jpg and on (1 per second), cuts.json
    breakdowns/{code}.md      one reel taken apart: facts from the script, then the Researcher's reading
```

`{code}` is the post's code from its link (Instagram) or its number (TikTok). Videos are never kept: they're downloaded to `study-tmp/` (next to `my-content-team/`, not inside it) and deleted after the study.

**Who reads what:**
- `breakdowns/`: **Brand Voice** builds the style guide from finished ones (`status: done`) instead of pulling winners again. Section 9 of each ("How to make one like it") is written for it. The Scriptwriter may open one to see how a template's reel was filmed. The Copywriter reads section 0's caption, section 1 and section 6 to see how the winning captions are built and how they ask.
- `playbook.md`: the Strategist (what to post), the Scriptwriter and Copywriter (how winners open, how long they run, how they end).
- `stats.md` and `dashboard.html`: the owner. The Researcher copies each account's normal and verdict into `competitors.md`.

**Breakdown front matter** (other teammates can count these): `status` (`stub` or `done`), the measured lines (`account`, `views`, `normal`, `score`, `likes`, `comments`, `length_s`, `cuts`, ...), then `format` and `hook_type` (words from `formats.md`), `topic` and `cta`.

**In chat** (no folders): the study comes as file blocks named `study-{handle}-stats.md`, `study-playbook.md`, and so on, with no pictures.

---

## analytics/ folder

Made by the Data Analyst's **Full account breakdown** (Composio connected, Claude Code or Cowork).

```
my-content-team/analytics/
  2026-11-04-instagram.json   one saved pull per date, never edited (the next pull is compared with the newest older one)
  dashboard.html              the full account breakdown page (open it in a browser); made by the Data Analyst's script from its template, replaced on every pull
```

Other teammates read the numbers from `results-log.md` and `performance-brief.md`, never from these files. In chat (no folders) the pull comes as a file block named `analytics-{date}-instagram.json`, and the owner pastes it into the dashboard page.

---

## script-templates.md

Written by the Content Researcher (Study accounts), one template per winning reel, each with a short version (20 to 45 seconds, the default) and the full skeleton. Read by:
- the **Scriptwriter**, which fills the blanks with the owner's facts only and uses the short version unless the owner asks for a long video;
- the **Repurposer**, which fills them with the ideas from a long piece (credited when it isn't the owner's) plus the owner's facts;
- the **Copywriter**, which names the template a video was built on in its post file (`Built on: template {N} (...)`, copied from the card) and may use a template's lines as the shape of a text post or carousel (fresh words, never a run of 5 or more of the template's words).

Templates keep the real lines with `[blanks]`, never beat labels. Numbers never change once given (the Scriptwriter, Repurposer and Copywriter name them: "built on template 3"); new ones go at the end.

````markdown
# Script templates
Last updated: YYYY-MM-DD
Made from: {N} winning reels from {accounts}. Fill the [blanks] with your own facts. Keep the lines, change what's in brackets.

## Template 1: {a plain name, e.g. "Call out who it's for, then what you're doing about it"}
- Hook type: {formats.md word}
- Format: {formats.md word}
- Length: the reel ran {N} seconds. Short version about {N} seconds, full version about {N} seconds
- From: @{handle}, score {N} ({views} ÷ normal {N}), breakdown `study/{handle}/breakdowns/{code}.md`
- Best for: {which kind of post, in plain words; "needs you on camera" if it does}

Short version (20 to 45 seconds, the one to use by default):
```
If you're [who the viewer is] and [the problem they have], here's what I'm doing about it.
[the strongest lines of the middle, 3 at most]
[your call to action]
```

Full version (for a long video):
```
If you're [who the viewer is] and [the problem they have], here's what I'm doing about it.
[every line of the skeleton, in order]
[your call to action]
```
(A reel already under about 45 seconds: one block and the line "Short and full are the same.")

## Template 2: ...
````

---

The other files (`competitors.md`, `research-notes.md`, `idea-bank.md`, `content-plan.md`, scripts, posts, `results-log.md`, `performance-brief.md`) each have their layout in the skill that writes them.
