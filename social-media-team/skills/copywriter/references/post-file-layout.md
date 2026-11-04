# The Copywriter's files

The Copywriter writes one kind of file (`posts/`) and changes one cell in another (`content-plan.md`). Other teammates read these, so keep the layouts exact.

---

## posts/{date}-{short-name}.md

- **One file per post.** A caption pack for one video is one file, with one section per platform.
- **Date:** the posting date from `content-plan.md` (`YYYY-MM-DD`). If the post isn't in the plan, use today's date.
- **Short name:** copy it exactly from the "Short name:" line in the post's brief in `content-plan.md`, so the Scriptwriter, the Copywriter and the Data Analyst all use the same one. Only when the post isn't in the plan, make one: 2 to 5 lowercase words joined with hyphens, taken from the post's title. Example: `posts/2026-11-04-tyre-check.md`.
- **In a Claude Project** (no folders): name it `posts-{date}-{short-name}.md`.
- **In chat with no file saving:** (only when you're handing over a post file; a quick draft that isn't a file gets no saving words) the file has code blocks inside it, so wrap the whole file in a fence of four backticks (````), with the file name as a heading above it. Each caption or slide stays inside it in its own normal code block. Then give the keep-it words from house rules section 4.
- **Same post again:** update the existing file. Don't make a second one.

### The header (every post file starts like this)

```markdown
# {Post title}
Date to post: {YYYY-MM-DD | not planned}
Type: {caption pack | text post | photo post | carousel}
Platforms: {e.g. Instagram, TikTok}
Structure: {name from post-structures.md} (for the team only, never in the post)
Built on: {template {N} (@{handle}, score {N}), copied from the filming card or the template | none}
Call to action: {e.g. "book link in bio" | "Comment GUIDE (DM tool, works on Instagram)"}
Offer post: {yes | no}
From: {content-plan.md P04 "{title}" | scripts/{file} | the owner's idea in chat | the owner's draft}
Status: {idea | scripted | filming | ready | posted}
Captions: {written | written, waiting for {what} | waiting for your OK | not written yet}
Last updated: YYYY-MM-DD
```

**Built on** is `none` unless the post was built on a script template (`writing-from-the-study.md`): copy the filming card's `Built on:` line exactly, or the template's number and "From" tag for a text post or carousel shaped like one. It's the only header line that may name a studied account, and it never goes into a caption.

**Status** uses the plan's status words only (`idea`, `scripted`, `filming`, `ready`, `posted`), plus the reason the Strategist adds when a format change sends a post back to `idea` (drop it once the status moves on), and matches the post's row in `content-plan.md` after you've finished (see the table at the bottom of this file). So a video whose captions are done but which isn't filmed yet keeps its plan word, for example `filming`. It becomes `ready` when the owner says it's filmed. A post that isn't in the plan follows the same rule: `ready` if nothing needs filming or the owner says it's filmed, otherwise `scripted` if there's a script, else `idea`. The owner or the Data Analyst changes it to `posted`.

**Offer post** is `yes` only by the team's offer post definition in `files-layout.md` (a price, a deadline, open spots or a discount, or a main message that pushes to book). A booking line at the end alone is `no`.

**Captions** is `not written yet` only on a file made in Visual hooks mode before any caption exists (its `Call to action:` line says `not written yet` too). **Captions** is `written` once the captions are done. If the post still has a blank the owner must fill, write `written, waiting for {what}` (for example `written, waiting for your price`) and keep the Status as it is: a post with an unfilled blank isn't `ready`. If you changed the post so it no longer matches its plan title (for example an offer turned into a helpful post), write `waiting for your OK` until the owner says yes, then `written`.

**`## Ready to post` or `## Draft, needs your answer`.** A caption, slide or platform section with any unfilled blank, or a post still waiting for the owner's OK, goes under `## Draft, needs your answer`, never under `## Ready to post`. Each code block holds only the text the owner pastes (the platform name is the `###` heading above it, never a line inside the block). No internal notes in the file ("Leak check done", check scores). If every section has a blank, the file has only the Draft heading; if some do and some don't, it has both, each heading used once (group the sections, never alternate them). Once the owner fills the blank, move that section under `## Ready to post`.

### Caption pack, text post or photo post

````markdown
{header}

## First line options
1. {option} (used)
2. {option}
3. {option}
Why 1: {one short line}

## Visual hooks
(video caption packs only; leave this heading out for text, photo and carousel posts)
In use: {from your filming card | ours | alternative A or B, your pick (YYYY-MM-DD)}
- Text on screen: "{5 to 10 words}"
- First frame: {one line}
- From: {your filming card | template {N} | your winner | a winner you studied | fresh, not proven yet}

Alternative A
- Text on screen: "{5 to 10 words}"
- First frame: {one line}
- From: {...}
- Why it might work: {one line}

Alternative B
- {same four lines}

## Ready to post

### {Main platform}
```text
{the full caption}
```

## Draft, needs your answer
(only for sections with an unfilled blank; leave this heading out when there are none)

### {Next platform}
```text
{the full caption, with its [blank]}
```

## Photo to use
{photo posts only: one line, or "the owner's choice"}

## Blanks to fill
- `[your price]`: in the {platform} caption, line {N}. {what to put there}
(or "None")

## Notes
- {anything the owner should know: a call to action you changed from the script, a voice guide that's missing, an offer you turned into a helpful post, the caption shape taken from the study}
(or "None")
````

**Notes stay true.** When the Status changes, rewrite or remove any Notes line it makes untrue in the same edit, such as "isn't filmed yet" once the post is `ready` or `posted`.

For a caption pack, the first line options are for the main platform's caption. For YouTube Shorts, the code block holds the title on the first line, then the short description if there is one.

### Carousel

````markdown
{header}

## Cover options
1. {option} (used)
2. {option}
3. {option}
Why 1: {one short line}

## Ready to post

### Slide 1 (cover)
```text
{headline}
{one short line, optional}
```
Picture: {one line}

### Slide 2
```text
{numbered headline}
{one short line}
```
Picture: {one line}

{...slides 3 to 6 or 7, same shape...}

### Last slide (call to action)
```text
{the call to action}
```
Picture: {one line}

### Caption ({platform})
```text
{short caption that repeats the cover promise and the same call to action}
```

## Blanks to fill
{as above}

## Notes
{as above}
````

### Visual hooks only

A file made in Visual hooks mode for a post that has no file yet: the header (with `Captions: not written yet` and `Call to action: not written yet`), then `## Visual hooks`, then `## Notes`. When the captions are written later, fill in the rest of the caption pack layout in the same file. The plan status never changes for visual hooks alone.

### Rewrite

Same as a text post, with one extra section right after the header:

```markdown
## What I changed
- {plain line}
- {plain line}
```

and `From: the owner's draft`.

---

## content-plan.md: the one cell the Copywriter changes

The Content Strategist owns this file and its layout. The Copywriter only reads it and changes the **Status** of posts it finished.

**How to find the row:** match the post number (`P04`), the short name in its brief, the posting date and the title. If two rows could match, ask the owner which one.

**What to change.** `ready` means everything needed to post exists. For a video that's filmed **and** captioned. The owner tells us when a video is filmed. Captions alone don't make a video `ready`.

| Row's status now | After the Copywriter finishes it |
|---|---|
| `idea`, `scripted` or `filming` (text post) | `ready` |
| `idea` (photo or carousel post) | `ready` once the owner says the photo exists; until then it stays `idea` and you say what photo it waits for |
| `idea` (video, no script yet) | stays `idea`. List it as waiting for the Scriptwriter |
| `scripted` or `filming` (video), not filmed yet | stays as it is (the post file's Status says the same word). Tell the owner: the captions are done, and it becomes ready once it's filmed |
| `scripted` or `filming` (video), the owner says it's filmed | `ready` |
| any status, but you changed the post so it no longer matches its plan title | stays as it is, and the post file says `Captions: waiting for your OK`. Flag it; set `ready` only after the owner says yes |
| any status, but the post has an unfilled blank | stays as it is, and the post file says `Captions: written, waiting for {what}`. Set `ready` once the owner fills it |
| `ready` | stays `ready` (update the post file if you rewrote it) |
| `posted` | never touch it |

- Change only the Status cell. Don't reword titles, briefs or tags. Don't reorder rows.
- **Never add a row.** Only the Content Strategist adds rows (the Repurposer may add some at the bottom of a week). If the post isn't in the plan, or the owner wants extra posts in it, write the post file and point to /content-strategist.
- Update the plan's "Last updated" line to today's date, if it has one.
- If the plan has no Status column, don't add one. Tell the owner in one line, and mention it to /content-strategist.
- If you turned an offer into a helpful post, or changed a post in any other way so it no longer matches its plan title, don't change the plan's title or tag. Flag it in the reply and the post file's Notes, and leave the Status as it is until the owner says yes.

**In chat with no file saving:** for one post, give a one-line change ("In content-plan.md, change the status of Tyre check to ready"). For a Week batch, give the whole updated `content-plan.md` in its own code block at the end and say: "Delete the old `content-plan.md` from your Project files first, then add this one."

---

## A filled example (made up)

Business: Spoke & Wheel, a bike repair shop. Main platform Instagram, also Facebook. No comment-to-DM tool. Books by text on 555-0100. Writes in short, friendly sentences, one emoji at most.
The plan has it as P05 with the short name `tyre-check`, so the file is `posts/2026-11-04-tyre-check.md`. A text post needs no filming, so its status is `ready`.

````markdown
# Tyre check in 2 minutes
Date to post: 2026-11-04
Type: text post
Platforms: Instagram, Facebook
Structure: Problem, fix, proof (for the team only, never in the post)
Built on: none
Call to action: "text 555-0100"
Offer post: no
From: content-plan.md P05 "Tyre check in 2 minutes"
Status: ready
Captions: written
Last updated: 2026-11-01

## First line options
1. Flat tyre again? It's probably not a puncture. (used)
2. A 2-minute check that keeps your rides flat-free.
3. Your tyres lose air even when the bike's just sitting there.
Why 1: it names the exact thing your customers complain about.

## Ready to post

### Instagram
```text
Flat tyre again? It's probably not a puncture.

Tyres lose air slowly, even parked. Soft tyres pinch and go flat.

Once a week, squeeze the tyre. If it gives easily, pump it to the number on the side of the tyre.

Takes 2 minutes. Still going flat? Text 555-0100 and bring it in 🚲
```

### Facebook
```text
Flat tyre again? It's probably not a puncture.

Tyres lose a little air every day, even in the shed. A soft tyre pinches on the first pothole and that's your flat.

Once a week, give it a squeeze. If it gives easily, pump it up to the number printed on the side.

Still going flat after that? Text 555-0100 and we'll have a look.
```

## Blanks to fill
None

## Notes
None
````
