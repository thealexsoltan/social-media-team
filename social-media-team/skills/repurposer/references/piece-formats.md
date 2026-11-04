# How to write each piece

Every piece starts from a numbered moment (an idea from the long piece). When the long piece is the owner's own, keep their words. When it's someone else's or a research paper, write in the owner's voice and credit the source (`credit-rules.md`). Either way you can shorten, reorder and add a hook, a [SHOW] note and a call to action. You can't add facts.

## The default mix

The owner picks how many pieces (10 if they don't say). The mix depends on whether `script-templates.md` exists; the table is in `filling-templates.md`. Without templates, for 10:

| How many | Piece |
|---|---|
| 4 | Short video scripts, each with its captions |
| 4 | Posts (text post, photo caption or quote post) |
| 1 | Carousel outline, 5 to 7 slides |
| 1 | Email or newsletter blurb, only if the profile or the owner mentions email or a newsletter. Otherwise one more post |

Swap the mix to fit the owner:
- **Not on camera** (profile says "no"): keep 4 scripts, but write them faceless, in the formats `Hands at work`, `Voice over clips`, `Text on screen only` or `Screen recording` from `formats.md`: the job, the place, the product. Say so in each script's [SHOW] notes. Never use `Talking head`.
- **Doesn't post video at all**: 2 scripts, 6 posts.
- **Only on LinkedIn or Facebook**: still 4 scripts if they film, but aim the posts at those platforms.
- **The owner asked for a different mix**: do what they asked. Keep the total at 10 unless they said a number.

Spread the posts over the platforms in `business-profile.md`. The main platform gets the most. Never write for a platform the owner doesn't use.

Two pieces can come from the same moment if they're different formats (a tip as a script and as a carousel is normal). Don't write the same piece twice with new words, never repeat a sentence across pieces, and don't pick a moment whose idea repeats a post already in `content-plan.md` or `posts/` (same point or same payoff, even told as a story, and that goes for a single slide or line inside a piece too): choose another moment instead.

---

## 1. Short video script

**`script-templates.md` exists:** build each script on the template that fits its idea, following `filling-templates.md`, and add the `Built on: template {N} (@{handle}, score {N})` line. The rest of this section still applies (length, shape, [SHOW] notes, plan tag).

Use the filming card layout from `script-shape.md`. It can be shorter than a full card:
- 15 to 45 seconds, about 40 to 110 spoken words (a template's short version runs 20 to 45)
- the four hooks, 2 or 3 beats, the payoff, one call to action
- a `Shape:` line, picked from the video shapes in `script-shape.md` by what the moment does (a list of warning signs is "Signs to watch for", a belief being corrected is "Myth"); `Other` only when no shape fits, and a `Job:` on each beat row, written for this video in a few words. Jobs and shape names never appear in anything said or shown
- "Filming notes" can be one line
- Plan tag: only when `content-plan.md` exists. Then `TEST`, unless `results-log.md` or `performance-brief.md` shows this same idea was one of the owner's winners, then `REPEAT`. Use the same tag in the content plan row. No `content-plan.md`: leave the Plan tag line out of the script.
- Format, for the plan row and the pieces table: pick the word from `formats.md` that matches what the script shows (`Talking head`, `Hands at work`, `Voice over clips`, `Text on screen only` and so on)

How to build it from a moment:
- **Spoken hook**: the template's first line with its blanks filled, or (no template) the owner's own sharpest line from that moment, trimmed. Turn "I" into "you" if it still sounds like them. From someone else's piece or a paper: the owner's words about the idea, with the credit (`credit-rules.md`).
- **Beats**: the template's lines, or the owner's own sentences, cut to one breath each.
- **Payoff**: the answer or the result the source actually gave. If the source never gave the result, don't make one up. Pick a different moment.
- **[SHOW] notes**: real things. If the owner showed something in **their own** original video, reuse it ("cut from the original at 04:12"). Never reuse footage from someone else's video. Otherwise simple shots they can film: hands working, the before, the tool, a text pop-up. A research number goes on screen with its short source ("a 2023 study of 1,204 nurses").
- Respect "Never say or show" in the profile (faces, house numbers, kids, and so on).

**In a chat reply**, wrap the whole filming card in one code block (a four-backtick fence if the card has blocks inside). **A saved card file** in `scripts/` has no fence around it: it's plain markdown in the Scriptwriter's layout, like every other card.

## 2. Posts and captions

Pick a shape from `post-structures.md`. Never show the shape's name in the post. Follow `caption-rules.md` for what a caption does and how each platform likes it.

Kinds of post you can make (the format word for the plan is in brackets, from `formats.md`):
- **Text post**: a story, opinion or tip, written out (`Text post`).
- **Photo caption**: say which photo to use, picked from things the owner would already have ("a photo of a before and after you already have") (`Photo`). Its plan row stays `idea` until the owner says the photo exists (`repurposed-file.md`).
- **Quote post**: one strong line from the source as the words on the image, plus a short caption (`Photo`). From someone else or a paper: under about 15 words, in quotation marks, with the name on the image (`credit-rules.md`).
- **Captions for a script**: every script comes with its captions, one per platform the owner uses, written the Copywriter's way (`caption-rules.md`). They belong to that script's piece and post, so they never get a plan row of their own and don't count as a separate piece.

Start each block with the platform and kind on the first line outside the code block, like: `Facebook, text post, from moment 2`.

## 3. Carousel outline

A swipe post (format `Carousel`). 5 to 7 slides. One idea per slide.

```text
Slide 1 (cover): {under about 12 words, says what they'll get}
Slide 2: {one point, up to about 25 words}
Slide 3: ...
Slide {last}: {one call to action}

Caption: {2 to 4 lines, then the same call to action}
Look: {one line, e.g. "your own photos as backgrounds" or "plain light background, big text"}
```

A carousel that needs the owner's photos waits at `idea` in the plan until they say they have them. Plain text slides need nothing, so it can be `ready`.

Steps and tips moments make the best carousels. Use the owner's words on the slides. A finding from a paper keeps its exact number and short source on its slide, and the full source on the last slide or in the caption (`credit-rules.md`).

## 4. Email or newsletter blurb

```text
Subject: {option 1}
Subject: {option 2}
Preview line: {the short line that shows after the subject}

{80 to 150 words in the owner's written voice. One idea from the piece,
told like a note to a customer. One link or one next step at the end.}
```

Only write it when the profile or the owner mentions email or a newsletter. If neither does, skip it and write one more post in its place.

---

## Calls to action

Use the team rule in `caption-rules.md`, one per piece, never two. What's extra for repurposing:
- "Comment {WORD}" only on the platforms the profile says the DM tool works on, and only if the owner has something real of their own to send (a checklist, a guide, the steps). Never promise a thing the owner didn't make, and never send someone else's guide or paper as theirs. On other platforms, use their booking route or a soft call to action.
- The email blurb ends with one link or one next step, not a comment word.
- If the profile doesn't say where people book, use `[your booking link]`.

## Gaps

If a piece needs something the source didn't give (a price, a date, a result, a number), leave a gap like `[your price]` and list it under "Gaps to fill" at the end. Never fill it yourself.

## A made-up example (a bakery, one moment, one script)

The bakery has a `content-plan.md`, so the card keeps its Plan tag line.

Moment 3 (tip, at 02:10): "Don't put bread in the fridge. The fridge makes it go stale faster. Freeze it in slices and toast it straight from frozen."

```markdown
# Stop putting bread in the fridge
Short name: bread-fridge-myth
From the plan: P07
Format: Hands at work
Hook type: Warning
Shape: Myth
Platform: Instagram Reels
Length: about 20 seconds
Plan tag: TEST

## The four hooks
- First frame: a hand putting a loaf into a fridge, then stopping
- First sound: the fridge door opening
- Text on screen: "Your fridge is making your bread stale"
- Spoken: "Don't put bread in the fridge."

## Script
| Part | Say | [SHOW] |
|---|---|---|
| Hook | "Don't put bread in the fridge." | Hand pulls the loaf back out |
| Beat 1. Job: why the fridge is wrong | "The fridge makes it go stale faster." | Close-up of a dry slice |
| Beat 2. Job: what to do instead | "Freeze it in slices..." | Slicing, bag going into the freezer |
| Payoff | "...and toast it straight from frozen." | Toast popping up |
| Call to action | "Fresh loaves are out at 7. Link in bio." | The shop counter |

## Payoff
"...and toast it straight from frozen."

## Call to action
"Fresh loaves are out at 7. Link in bio."

## Filming notes
- Shots to grab: fridge, slicing, freezer, toaster. Props: one loaf.
```

Notice: every spoken line is the owner's own. The shape fits what the moment does (it busts a belief, so Myth), and this short card has two beats. The call to action uses only facts from their profile.

## A made-up example (a nurse career coach, a research paper, a template)

The owner's `script-templates.md` has a made-up Template 2:
```
[a surprising number] of [people like your viewer] [do the thing].
Here's why that matters: [the reason].
So [what to do about it, one line].
[your call to action]
```

Moment 4 (finding, page 9, Results; credit: Lee and colleagues, 2023, a made-up journal): "Of the 1,204 nurses who left hospital work, 61% said they had waited more than a year before applying anywhere."
The owner's profile ("Owner's answers"): "the waiting is the worst part. you don't need a perfect plan, you need one application out this month."

The card's spoken lines:
- "61% of nurses in a 2023 study waited more than a year before applying anywhere."
- "Here's why that matters: the waiting is the worst part."
- "So you don't need a perfect plan, you need one application out this month."
- "Link in bio for a free call."

Header lines: `Shape: Myth`, then `Built on: template 2 (@{handle}, score {N})`. Text on screen with the number: "1,204 nurses who left, 61% waited over a year (2023 study)". The caption names the paper in full. Notice: the template's lines and connector words stay, the number is exactly as the paper gives it with who and when, and the lines about what to do are the owner's own words, not the paper's.
