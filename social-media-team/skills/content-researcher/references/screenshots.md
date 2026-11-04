# Screenshots: what to ask for and how to read them

Screenshots are the **fallback** for reading other accounts. The main route is the Apify connector (`connectors.md`), because it reads every recent post's views for you. Use screenshots when Apify isn't connected, its free credit is used up for the month, the platform has no Apify tool picked (anything but Instagram and TikTok), or a pull came back short. Screenshots are still the only way to see the first frame of a video and anything on the owner's screen that a pull doesn't bring.

## Why screenshots, not links

| What the owner sends | What you can get from it |
|---|---|
| A link, in chat | Only the page title ("Instagram", "TikTok"). Nothing else. Don't pretend otherwise |
| Screenshot of the **Reels tab** (Instagram) or **profile grid** (TikTok) | The view count of each recent video, pinned posts, followers, and the cover of each video |
| Screenshot of **one post** | Caption, likes, comments, date, the cover or the frame on screen. **No views** on Instagram posts, no plays on TikTok video pages |
| Screenshot of the first seconds with **captions turned on** | The spoken first line |
| The owner typing what they hear | Spoken first line, first sound, music or no music, length |
| Instagram's main grid (the square photos tab) | No view counts. Ask for the Reels tab instead |

Only the grid shows every video's views, so without it there's no normal and no fair "winner". Raw views alone mean nothing between accounts of different sizes.

Other platforms: YouTube Shorts show views on the channel's Shorts tab. On Facebook, use the page's Reels tab if numbers show under each reel. If they don't, say so and suggest studying the same kind of account on Instagram or TikTok instead. LinkedIn doesn't show a grid of views, so don't qualify LinkedIn accounts by views.

## What to tell the owner (copy this, fill the blanks)

> For each account, send me:
>
> 1. **One screenshot of their video grid.** On Instagram, open their profile and tap the Reels tab (the play button). On TikTok, their profile already shows it, just leave it on the first tab, not "Popular". The number under each video is its views. Scroll so I can see at least 12, two screenshots is fine.
> 2. **For their 2 or 3 best videos:** a screenshot of the post with the caption showing.
> 3. **If someone talks in the video:** type the first sentence they say, or turn on captions and screenshot the first 2 seconds. If it's only music, just tell me that.
>
> A link on its own isn't enough for me to see anything, the screenshots are what I read.

Ask once, in one message. If the owner already sent accounts or screenshots in this chat (the Content Team's kick-off asks for them), said that's all they have, or said no (in this chat, or a "Declined questions" line in `team-status.md` whose ask again date hasn't come), don't ask again. If they send less, work with what came and list what's missing.

## Reading a grid

1. **Count what you can read.** Say it: "I can read 16 view counts." Blurry or cut-off numbers are left out, not guessed.
2. **Turn short numbers into full ones.** 1.2K = 1,200. 26.3K = 26,300. 1.1M = 1,100,000.
3. **Pinned posts** (a pin icon, always first in the grid) are old all-time hits. Leave them out of the normal and list them under "All-time hits".
4. **Newest posts** sit at the top left. A grid doesn't show dates. If the owner says a post is under 3 days old, or the post screenshot shows a date under 3 days ago, leave it out. If you can't tell, say: "The newest 1 or 2 may still be growing."
5. **TikTok "Popular" tab** sorts by most views, so the middle number is far too high. Use it only to spot all-time hits. The normal comes from the default (newest first) grid.
6. **Find the normal**: use every readable post left after steps 3 and 4, up to 30. Put the numbers in order and take the middle one. With an even count, take the two middle ones and halve their total. Show the list in order so the owner can check.
7. **Score each post**: views ÷ normal, one decimal. 2.0 or more is a winner. Winners can be any post used for the normal. Say the count against the posts used: "4 winners in the last 15."
8. **Look at the covers** for clues you can actually see: a face or no face, words on the cover, the same look repeated (same opening shot or same style of text on every video, which often means they found something that works). Say "from the covers it looks like", because a cover can be picked by the creator and isn't always the first frame.
9. **Fewer than 9 readable posts**: "small sample", verdict Maybe at most.

## Worked example (made up)

> I can read 16 view counts, plus 3 pinned reels (412K, 96.1K, 58K) that I've left out as all-time hits. You said the newest one went up yesterday, so I've left that out too. That leaves 15.
>
> In order: 2,200, 2,500, 2,700, 2,800, 2,900, 3,000, 3,100, **3,200**, 3,300, 3,400, 3,600, 7,900, 8,800, 14,600, 26,300
>
> Normal: 3,200 (the middle one).
>
> Winners:
> - 26,300 ÷ 3,200 = 8.2
> - 14,600 ÷ 3,200 = 4.6
> - 8,800 ÷ 3,200 = 2.8
> - 7,900 ÷ 3,200 = 2.5
>
> 4 winners in the last 15. You said they post 3 or 4 times a week, and from the covers it looks like hands-at-work videos you could film in your van.
>
> **Verdict: Keep** (same niche). Steady winners, and their best ones are about coat care, same as yours.

If neither you nor the owner could tell how often they post, the same grid would get **Keep (posting frequency not checked)**.

## Where numbers came from

Mark every number with its source in the notes: `grid screenshot`, `post screenshot`, `owner typed it`, or `Apify`. If two sources disagree, trust the grid and say so.

## With the Apify connector

Everything about pulling, confirming the account list first, which number to use and what a pull misses is in `connectors.md` ("Apify"). Once the posts are in, read them like a grid ("Reading a grid" above): say how many came back, leave out pinned posts (marked `isPinned`) and posts under 3 days old (the pull has dates, so check them), then find the normal and the winners the same way, up to 30 posts. Two things to add:
- If you also have a grid screenshot, compare. If the newest reels are missing from the pull, say so and trust the grid.
- A pull doesn't give you the first frame, the spoken words or the first sound. In Cowork or Claude Code, offer **Deep study** (`deep-study.md`) to read them from the videos. Otherwise, for winners, ask for a post screenshot and the first spoken line (unless the owner declined screenshots), or write `not seen`.
- An Instagram pull has no follower count, which the whole-account check needs (`outlier-score.md`). Read it from a grid screenshot's header, or ask the owner to read it off the profile. Ask once.
