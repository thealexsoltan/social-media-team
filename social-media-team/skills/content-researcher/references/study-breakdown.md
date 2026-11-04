# Breaking down a studied reel, and the playbook

The study script already measured everything it can and wrote it into the stub: views, score with its sum, likes, comments, length, cuts, cuts per 10 seconds, the sound, the caption and every spoken line with its time. Your job is to **read the pictures and explain**. Precision beats nice writing.

## Rules

- Only write what's in the stub or visible in the pictures. Never invent text, times or numbers. Something you can't see is `not seen`.
- Read `hook.jpg` and **every** `seconds-*.jpg` the stub lists. Open a full-size `hook-{time}s.jpg` only to check small text. Tiles run left to right, top to bottom. If the time is printed in the corner, use it; if not, the stub lists each sheet's tile times: use those, never guess a time from a tile's position. One picture per second can miss very short text: say so if it matters.
- The spoken words were machine heard and can be wrong. When words burned into the video show the right spelling, trust those and say so.
- **Text hook vs captions:** words that pop up a few at a time and match the speech are captions of the speech, not a text hook. A text box that stays on screen (a title, a headline, a label) is the text hook.
- **First sound:** speech starts in the first half second (by the transcript's first time) = `voice, talking from the start`. Otherwise use the stub's sound line: "Original audio" means their own sound, a song name means a track. A noise you can't confirm is `not seen` (Claude can't hear the video).
- Hook type and format use only the words in `formats.md`.
- Their words are fine in sections 1 and 2 (that's the research). From section 8 on, describe the move, never their sentences, stories, names or numbers.
- No long or short dashes as punctuation. Plain words.
- **Hard limit: 300 to 500 words for sections 1 to 9, tables included.** Count before you save. Over 500: cut the words-on-screen table to the lines that matter (titles, labels, the first 2 or 3 captions), shorten shots and pacing to 2 or 3 lines each, and keep 2 bullets in sections 7 and 8. Section 0 (made by the script) doesn't count.
- **Who is talking:** the `first_line` was machine heard. Check in the hook frames that the person on screen is the creator. If a guest, a clip or a voice off screen speaks first, say so in section 1 ("first voice: a guest, then the creator at 2.5s").

## Filling the stub

Front matter: change `status: stub` to `status: done`. Leave the measured lines as they are. Fill:
- `format`: one word set from `formats.md` (e.g. `Talking head`)
- `hook_type`: one from `formats.md`
- `topic`: 3 to 6 plain words
- `cta`: the exact ask, word for word, or `none`

Keep section 0 as it is. Fill each section under its heading:

1. **Hook (first 3 seconds)**: four short lines plus one, each with where it came from:
   - Spoken: "{first sentence}" (machine heard), or `no talking`
   - Text on screen: "{word for word}" (video still), or `none`
   - First frame: {what we see, one line} (video still)
   - First sound: {voice, a track, their own sound} (music info, or the transcript's first time)
   - Why it stops the scroll (best guess): one line tied to something you can see or hear.
2. **Words on screen**: a small table `| Time | Text | Kind |`. Kind is `title`, `caption of the speech`, `label`, `sticker` or `list`. Captions of the speech: say so once and give the first 2 or 3 as examples, don't copy them all. Leave out background text (a shirt, a poster, packaging).
3. **Shots and setting**: how close the camera is, held or on a stand, the angle, the place, the light, props, any other clips cut in, any before and after build (with times).
4. **Pacing**: read the measured cuts: where the edit removes pauses, where it speeds up or slows down, how long the longest shot holds and what happens in it. Cut counts come from a tool: if the pictures disagree, say so.
5. **The parts of the video**: `| Time | Part | What happens |`, 3 to 7 rows, times from the transcript. Plain part names ("the claim", "the first tip", "the proof", "the ask").
6. **Call to action**: what's said, what's on screen, what the caption asks, and when it lands.
7. **Why it worked (best guess)**: 2 to 4 bullets, each tied to something visible or heard in this reel. Score and normal from section 0. For a contrast post: why it did about normal, and what it lacks next to the winners.
8. **Steal this**: 2 or 3 moves the owner could copy, written as instructions ("Put the claim on screen in the first frame, then say it"). Moves only, never their words.
9. **How to make one like it** (Brand Voice reads this part):
   - How it's built: the opener, the middle and the ending, in your own words, with `[blanks]` where the owner's facts go.
   - The psychology: the feeling it uses (curiosity, "that's me", relief, surprise) and the pattern behind it (an open loop, a number that sounds too big, naming the viewer's exact situation).
   - What we'd need from you: the facts, story, belief or result this shape needs from the owner.
   - Points at: who a blame or contrast may and may not point at for this owner (never their own trade, partners or customers), or `nobody`.

## The playbook: `study/playbook.md`

Count, don't guess. Every line says "x of y reels" and names the reels behind it (account and score). A pattern needs 2 or more reels from 2 or more accounts; with one account, write "1 account, so a start, not a rule yet" at the top and keep the counts. Compare winners with the contrast posts wherever you can: that's the most useful part.

```markdown
# Playbook: what's working
Made: YYYY-MM-DD, by the Content Researcher
Built from: {N} reels ({W} winners, {C} normal posts for contrast) from {accounts, each with its normal}. Numbers from Apify, words machine heard, pictures read from the videos.

## In one line
{what the winners have in common, in one plain sentence}

## Hooks
- {pattern} ({x of y winners}: @handle 4.6, @handle 3.1)
- Text on screen at the very start: {x of y winners} vs {x of y normal posts}
- Spoken first line: about {N} words in the winners (middle), {N} in the normal posts

## Formats
| Format | Winners | Normal posts |
|---|---|---|

## Length and pacing
- Middle length: winners {N}s, normal posts {N}s
- Cuts per 10 seconds (by a tool): winners {N}, normal posts {N}
- {what the edit does, x of y}

## How the videos are built
- {parts in order, x of y}

## Calls to action
- {the ask as a move, x of y}

## Captions
- Length: winners {N} words (middle), normal posts {N}
- How the winning captions are built: {first line, middle, where the ask sits, sign-off, as moves, x of y}

## Topics
- {topic, x of y, accounts}

## What winners do that the normal posts don't
- {difference, with the counts on both sides}

## Per account
### @handle (normal {N})
{2 to 4 lines}

## Seen once only
- {a move from one reel: a test, not a rule}

## What we couldn't see
- {e.g. "Instagram shares and saves: not in the public data." "1 reel had no speech."}
```
