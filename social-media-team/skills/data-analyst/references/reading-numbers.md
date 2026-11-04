# Reading the owner's numbers

Three ways numbers arrive: an export file, screenshots, or typed numbers. All three end up as the same rows in `results-log.md`.

## Before you read anything

Ask (once, in one message, only what you don't know yet):
- Are these **lifetime** numbers for each post, or only the last few days? Lifetime is what we want. If the file says "Lifetime" somewhere, you're fine. If only a short window was picked, older posts will look worse than they really are: say so and ask for a lifetime export.
- Was any post **boosted** with ads? Boosted views aren't fair to compare. Follow the boosted rule in `outlier-score.md`: leave it out of the normal, score it separately and mark it boosted (Score cell like `3.1 boosted`).
- Was any post deleted and reposted, or posted as a trial for non-followers? Note it, and ask whether to count it.
- **Did you film these as written?** Ask only when some of the posts have a card in `scripts/` or a file in `posts/`. One yes or no for the week. The answer decides whether the card's tags count as known (`from our card`) or as a guess (`from our card, not confirmed`). Details: `tags.md`, "Did they film it as written?".

## Export files (CSV)

Platforms rename columns now and then. Match by meaning, not exact words:

| Our column | Names you might see |
|---|---|
| Posted | Publish time, Published, Date posted, Created, Post time |
| Post text | Description, Caption, Title, Text |
| Format | Post type, Media type, Type (Reel, IG reel, Video, Carousel, Image, Photo) |
| Length | Duration, Duration (sec), Video length |
| Views | Views, Plays, Video views |
| Likes | Likes, Reactions |
| Comments | Comments |
| Shares | Shares |
| Saves | Saves, Saved, Favourites |
| Follows | Follows, New followers, Followers gained |
| Profile visits | Profile visits, Profile activity, Profile views |
| Link taps | Link clicks, Website taps, External link taps, Sticker taps |
| Link | Permalink, Link, URL |

Watch out for:
- **Reach is not views.** Reach counts people, views counts plays. Use views for the score. If a file only has reach, say so and use reach for every post the same way, and note it in the log.
- **Watch time** may come in milliseconds. Turn it into seconds (divide by 1,000) before you write it anywhere. We don't score on it, but it's fine to mention.
- **Blank cells or zeros that look wrong** (a post with 3,000 views and 0 likes): ask, don't fix it yourself. A blank cell is `not visible`, never 0.
- **Mixed formats.** Reels and photos behave differently. Score them together if that's all there is, but say how many of each there were, and compare like with like when you look for patterns.
- **Several platforms in one file.** Work out a separate normal for each platform. Never mix them into one normal.

After reading, say in one line what you found. A made-up example for a bike shop: "I read 22 posts from 2026-03-02 to 2026-04-11, all TikTok, 20 videos and 2 photo posts." This lets the owner catch a wrong file early.

## Screenshots

- Read only what's clearly on screen. A number that's cut off, blurry or hidden behind a button is `not visible`.
- Never read numbers off a chart's height. If the screen shows a graph without labels, say so.
- Watch for shortened numbers: "1.2K" means about 1,200, but you don't know if it's 1,150 or 1,249. Write `1.2K` in the log, use 1,200 for sums, and in the reply write "about 1,200" and say the sum is rounded.
- Put what you read in a small table before you analyse, and ask the owner to fix anything wrong. Don't make them wait for a separate step: carry on in the same reply.
- If you can't tell which post a screenshot belongs to, ask.

A screenshot of a profile grid usually shows only views on each tile. That's enough for the score, but not for follows or link taps. Say so.

## Typed or pasted numbers

Owners often type things like "the ladder one got about 900 views and a few comments". Log what's exact. For "about 900", log 900 and note "owner's estimate". For "a few comments", log `not given` and ask for the number if it matters for the goal.

## Matching to rows already in the log

- Match a post to its earlier rows by its link, or by its date plus caption. Then add a **new** row with the new check date. Never overwrite an old row.
- A post you've never seen before: add it to "What's in each post" too, after checking `scripts/` and `posts/` for its card and post file by short name (`tags.md`).
- If two posts have the same date and similar captions, ask which is which.
- If the owner says which plan post a row is, but the dates or captions don't fit (the plan post was meant for Thursday, but the only post that week went up on Monday with a different caption), say so plainly. Log the post under its own name from its own date and caption, and add "Which plan post is {post}?" to "Open questions for the owner" in `team-status.md`. Never force a match.

## Rounding

Work out each score, round it to one decimal, then pick its band from the rounded number. So 1.96 becomes 2.0, a winner, and 0.48 becomes 0.5, below normal (not a flop).

## The 3-day rule and post age

- A post younger than 3 days gets the score `too new`. Log its numbers anyway. Score it next week.
- Posts keep getting views for a while. A post checked at 5 days old isn't finished either. When you compare a 5-day-old post with 30-day-old ones, say "it's still young, this may go up".
- For each post, the latest check is the one that counts for the normal and the score.

## Things you never do

- Fill a missing number with a guess, an average or "probably about".
- Work out bookings, sales or money from views. If the owner wants to know what posts earned, ask them for the number of bookings, calls or sales, and where each came from if they know.
- Predict future views or followers.
