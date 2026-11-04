<!-- Copied from shared/methods/outlier-score.md by scripts/sync-shared.mjs. Edit the shared file, not this copy. -->
# Outlier score: the fair way to say "that post worked"

Raw views lie. 10,000 views is a flop for a big account and a hit for a small one. So we compare every post to **that account's normal**.

## The sum

1. Take the account's last 15 to 30 posts (the more the better, but never fewer than 9).
2. Leave out posts younger than 3 days. They haven't finished getting views yet. The same goes for a post whose only check was taken when it was under 3 days old: it stays out of the normal until it's checked again.
3. Leave out posts the owner paid to boost. Paid views aren't a fair comparison. Score them separately and mark them "boosted".
4. Find the **normal**: put the view counts in order and take the middle one (the median). Don't use the average: one huge hit drags the average up and makes everything else look bad.
5. For each post: **outlier score = its views ÷ the normal**, rounded to one decimal.

| Score | What we call it | What to do |
|---|---|---|
| 2.0 or more | **Winner** | Study it. Make more like it |
| 1.0 to 1.9 | Normal to good | Nothing special |
| 0.5 to 0.9 | Below normal | Note it, no alarm |
| under 0.5 | Flop | Check the hook first (see `four-hooks.md`) |

Show the sum so the owner can check it: "Normal for this account is 2,400 views. This reel got 9,100. 9,100 ÷ 2,400 = 3.8, so it's a winner."

## When every post does well (the whole-account check)

The outlier score only spots posts that beat their own account. It misses an account where **every** post does well. Example: a new account with 10 videos, 2 at 100,000 views and 8 at 80,000. Its normal is 80,000, so the best ones score 100,000 ÷ 80,000 = 1.3. No winners, yet the whole account is flying.

So after the per-post scores, always run two quick account checks. Use the same normal as above (same posts left out).

1. **Reach check:** normal ÷ followers. **2.0 or more** means a normal post reaches at least twice as many people as follow them, so the videos travel far past their own audience. "Normal 80,000 ÷ 3,000 followers = 26.7. Passes."
2. **Group check** (only when at least 3 **other** accounts on the same platform have a normal in `competitors.md`): normal ÷ the middle of those other normals. **2.0 or more** passes. "The other 4 normals in order: 1,900, 2,600, 3,100, 4,000. Middle: (2,600 + 3,100) ÷ 2 = 2,850. 80,000 ÷ 2,850 = 28.1. Passes."

If either check passes, **the whole account is winning**, even with no per-post winners. Show the sums. Write `not checked` for a check you can't do (no follower count, or fewer than 3 other normals) and say why. Never guess a follower count.

- Fewer than 9 posts for the normal: still give the result, but say "small sample" and check the account again once it has more posts.
- A whole account that's winning has no single posts to study. Study **what its posts have in common** instead: format, topic, how they open, length and call to action, each counted as "x of y posts".
- Big accounts in a broader niche often pass the group check just by being bigger. That's fine: it still tells you their normal post is worth studying.

## The owner's own account: is their style already working? (Brand Voice)

Brand Voice uses the same sum on the **owner's own** account to decide where to learn their voice from. It's a different question from the 2.0 bar above: that bar spots accounts worth copying, this one only asks "do your posts already work?", so the lines are lower.

**Reach** = the owner's normal ÷ their followers (same normal, same posts left out, and pinned posts left out too: they sit at the top for months and aren't a normal post).

| Reach | Plain meaning | Where Brand Voice learns from |
|---|---|---|
| 1.0 or more | A normal post reaches at least as many people as follow you | **Path A:** your own best posts |
| 0.3 to 0.9 | Your followers see it, but it doesn't travel much further | **Mixed:** your own words, the post shapes of winners in your niche |
| under 0.3 | Posts don't reach even a third of your followers | **Path B:** winners in your niche first, then a few questions about you |

- **5,000 view floor for path A.** A reach of 1.0 or more with a normal under 5,000 views is Mixed, not A. (200 followers and 400 views scores 2.0 but proves very little.)
- **Under 9 posts, or just starting:** path B. No sum needed.
- **Close to a line** (within 0.1): use engagement as the tiebreaker, (likes + comments + shares) ÷ views. 5% or more leans to the higher path. Without those numbers, ask the owner which path feels right.
- **X, LinkedIn and other text posts** reach far fewer of their followers than short video, so these lines are only a rough guide there. Say so and let the owner pick.
- **Show the sum and say it kindly**, as a fact about the posts, never about the person: "Your normal post gets 7,500 views and you have 300,000 followers. 7,500 ÷ 300,000 = 0.03, so a normal post reaches about 1 in 40 of your followers. Your audience is there, the posts just aren't reaching them yet."

Worked examples: 300,000 followers, normal 7,500 = 0.03, path B. 40,000 followers, normal 52,000 = 1.3, path A. 12,000 followers, normal 6,000 = 0.5, Mixed. 900 followers, normal 1,400 = 1.6 but under 5,000 views, Mixed.

## Pick the number that matches the goal

Views tell you about the hook. They don't tell you about the business. Rank by the number that matches what the owner wants:

| Goal | Rank by |
|---|---|
| Followers | follows per 1,000 views (follows ÷ views × 1,000) |
| Leads or DMs | comments and shares (comments are often people asking) |
| Bookings or sales | link taps, profile visits, DMs, then follows |
| Getting seen | views, using the outlier score |

When you only have views (for example a competitor's grid), use the outlier score and say that's all you can see.

## Two posts that look alike

The best lessons come from two posts with **the same topic** but very different results. Put them side by side and list every difference (first line spoken, text on screen, first frame, length, time posted). The difference that's left is your best guess at the cause. Say "best guess", not "proof".

## Where the numbers come from

- **The owner's own posts:** Instagram: Professional dashboard or the post's "View insights". TikTok: Analytics. A screenshot or an exported file is fine.
- **Someone else's account:** you can only see views where the platform shows them (the Reels tab on Instagram, the profile grid on TikTok). Ask for a screenshot of the grid.
- Never guess a number you can't see. Write "not visible" and move on.
