# Full account breakdown

The owner's whole Instagram account in one page: every number Instagram gives, each against its benchmark in green, yellow or red, the one step to fix first, the funnel in plain numbers, what's working and what's not, every reel against the account's normal, and the benchmarks with their sources. Pulled read only through Composio, saved, then shown as `my-content-team/analytics/dashboard.html`.

**One source of truth for the page:** `assets/dashboard-template.html` in this skill's folder. It is the dashboard page itself (its own code does every sum). Never rebuild it, restyle it or write HTML by hand. `scripts/dashboard.py` only copies it and puts the owner's saved pull into it.

## When

- **First run with Composio connected:** this is the default first job (before the first weekly report), because it needs nothing from the owner.
- Any time the owner says "pull my numbers", "full breakdown", "refresh my dashboard", "how is my account doing", "break down my whole account".
- Weekly, same day each week, if the owner wants it. The comparison with their own last pull is what matters most from the second pull on.

## Step 1: Connect check (one message, only what's missing)

1. **Is Composio connected?** Call `COMPOSIO_SEARCH_TOOLS` (read only) with a use case like "get my Instagram account insights" and look at the Instagram toolkit's connection status. No Composio tools at all: say so in one line, offer the connector (`connectors.md`, Composio section), and carry on with the paste route below. Never stop the job.
2. **Is Instagram connected in Composio?** If the toolkit has no active connection, ask: "Want to connect your Instagram to Composio now? You'll sign in to Instagram yourself in a window that opens." Only after a yes, start the Instagram connection with `COMPOSIO_MANAGE_CONNECTIONS` and let the owner sign in. Never remove, replace or change a connection that already exists.
3. **Which account?** If more than one Instagram account is connected, ask which one (list the handles) and pass that account on every call.
4. **Business or Creator?** The first call (`INSTAGRAM_GET_USER_INFO`) returns `account_type`. It must be `BUSINESS` or `MEDIA_CREATOR`. A personal account gets no insights: say "Instagram only shares these numbers with Business or Creator accounts. Switching is free: Settings, Account type and tools, Switch to professional account." Stop the pull there.

**Read only, always.** Never post, reply, comment, like, delete, archive, schedule or change anything on the account or in Composio, even if the owner asks in the same message. Say: "I can only read your numbers. I can write the caption for you to post yourself." The tools you may call: `COMPOSIO_SEARCH_TOOLS`, `COMPOSIO_GET_TOOL_SCHEMAS`, `COMPOSIO_MULTI_EXECUTE_TOOL` (with the `INSTAGRAM_GET_*` tools below only), and `COMPOSIO_MANAGE_CONNECTIONS` only to start a new connection the owner said yes to.

## Step 2: The pull (this recipe worked live on real accounts)

Run calls that don't depend on each other together with `COMPOSIO_MULTI_EXECUTE_TOOL`, up to 50 at once. If a tool name below doesn't exist, search Composio for the one that does the same job. TODAY is today's date in UTC (YYYY-MM-DD), or the owner's date if they gave one.

a) `INSTAGRAM_GET_USER_INFO`: ig_user_id "me", fields "username,name,account_type,followers_count,follows_count,media_count".
b) Twice, once with since = TODAY minus 28 days and once with since = TODAY minus 7 days, until = TODAY, period "day", metric_type "total_value", `INSTAGRAM_GET_USER_INSIGHTS` with:
   - metric ["views","reach","accounts_engaged","total_interactions","likes","comments","shares","saves","replies","reposts","profile_views","website_clicks"];
   - metric ["follows_and_unfollows"] with breakdown "follow_type" (keep only the FOLLOWER value, as "follows");
   - metric ["reach"] with breakdown "follow_type";
   - metric ["views"] with breakdown "follow_type".
c) `INSTAGRAM_GET_USER_INSIGHTS`, metric ["follower_count"], period "day", since TODAY minus 28 days, until TODAY. These are NEW followers per day. Each end_time belongs to the day before it. A 0 on the newest day is an unfinished day: write null.
d) `INSTAGRAM_GET_USER_INSIGHTS`, metric ["online_followers"], period "lifetime", since TODAY minus 3 days, until TODAY minus 1 day. It comes back empty without since and until.
e) `INSTAGRAM_GET_USER_INSIGHTS`, period "lifetime", metric_type "total_value", timeframe "this_month", once for each metric follower_demographics, engaged_audience_demographics, reached_audience_demographics, and each breakdown age, gender, country, city (12 calls).
f) `INSTAGRAM_GET_IG_USER_MEDIA`: ig_user_id "me", limit 100, fields "id,caption,media_type,media_product_type,is_shared_to_feed,timestamp,permalink,like_count,comments_count". Keep the newest 60 where media_type is VIDEO and media_product_type is REELS.
g) For each of those reels, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` with metric ["views","reach","likes","comments","saved","shares","total_interactions","ig_reels_avg_watch_time"], and a SEPARATE call with metric ["reels_skip_rate"], so a refusal can't break the first call. If a code sandbox is available, use it for these reel calls.

If a call fails because of one metric, run it again without that metric and add {"metric": name, "reason": a few words} to "missing". An empty answer is not an error: write null and add it to "missing". On a server error, wait 2 seconds and try once more.

**Rules for the numbers:**
- A number Instagram didn't return is **null, never 0**. Copy every number exactly; never estimate or round.
- hook = the first line of the caption, 80 characters at most. feed = is_shared_to_feed (false for trial reels). avg_watch_s = ig_reels_avg_watch_time divided by 1000. saves = saved.
- **Under 1,000 followers** reel insights may be refused: keep the reels anyway with likes and comments from the media list, views null, insights false, and set small_account to "under_1000".
- **Under 100 followers** Instagram hides audience numbers: set small_account to "under_100".

## Step 3: Save the pull

Write it as `my-content-team/analytics/{TODAY}-instagram.json` in exactly this shape (the page reads this shape; keep the `aicc-ig-v3` id as it is):

```json
{"schema":"aicc-ig-v3","pulled_at":"2026-11-04T15:20:00Z","source":"composio","account":{"username":"handle","name":"Name","account_type":"BUSINESS","followers":0,"following":0,"media_count":0},"windows":{"28":{"since":"2026-10-07","until":"2026-11-04","views":0,"reach":0,"accounts_engaged":0,"total_interactions":0,"likes":0,"comments":0,"shares":0,"saves":0,"replies":0,"reposts":0,"profile_views":0,"website_clicks":0,"follows":0,"reach_follower":0,"reach_non_follower":0,"views_follower":0,"views_non_follower":0,"views_unknown":0},"7":{"since":"2026-10-28","until":"2026-11-04","views":0}},"daily_follows":[{"date":"2026-10-06","value":0}],"online_followers":[{"date":"2026-11-01","hours":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}],"demographics":{"follower":{"age":{"35-44":0},"gender":{"F":0},"country":{"US":0},"city":{"Austin, Texas":0}},"engaged":{"age":null,"gender":null,"country":null,"city":null},"reached":{"age":null,"gender":null,"country":null,"city":null}},"reels":[{"id":"1","permalink":"https://www.instagram.com/reel/x/","posted":"2026-10-30T23:17:42Z","feed":true,"hook":"first caption line","views":0,"reach":0,"likes":0,"comments":0,"saves":0,"shares":0,"interactions":0,"avg_watch_s":0,"skip_rate":0,"insights":true}],"status":{"small_account":"no"},"missing":[]}
```

(Zeros above only show where numbers go. A real pull has the real numbers, and null where Instagram gave nothing.)

Instead of rebuilding the shape by hand you may save the raw answers: `{"pulled_at": ..., "today": ..., "calls": [{"tool_slug": ..., "arguments": ..., "response": {"successful": ..., "data": ...}}]}`. The script and the page both read that too.

A pull is never changed after it's saved. A new pull is a new file. Old pulls stay: they're what the next comparison uses.

## Step 4: Make the page

In Claude Code or Cowork, run the bundled script from the owner's working folder (the one that holds `my-content-team/`). `DASH` means the full path of `scripts/dashboard.py` in this skill's folder, in double quotes:

```
python3 DASH my-content-team/analytics/2026-11-04-instagram.json
```

It writes `my-content-team/analytics/dashboard.html` (the template with the owner's numbers inside, opening straight on them) and prints a summary: the 3 steps working, the 3 not working, the one to fix first (the page's own "primary bottleneck"), the reels (normal, best, worst), what Instagram didn't give, the comparison with the newest older pull in the same folder, and rows for `results-log.md`. **Every number you write in chat or in the files comes from that printout or the page, never from your own sums.** Pass `--today YYYY-MM-DD` when the owner gave a date. `--check` only reads the file and lists what's missing. The script then opens the page in the owner's default browser by itself (its last line starts `BROWSER:`).

Then check the page exists (Glob) and read the `BROWSER:` line. It says opened: tell the owner "I opened your dashboard in your browser." It says not opened or couldn't: tell them "Open `my-content-team/analytics/dashboard.html` in your browser (double-click it)." and give that path.

**In chat (no files, no script):** give the saved pull in one code block named `analytics-{TODAY}-instagram.json` with the keep-it steps (house rules section 4), and tell the owner to open `dashboard.html` (in this repo, or the file that came with your purchase) in your browser, press paste instead, and paste the block the Data Analyst gives you. (Cowork without the script: the same.) The page works the numbers out itself. Do the summary below from the page's numbers only if the owner pastes them back; otherwise give only what you can read straight off the pull (followers, views, reach, profile visits, link taps, follows for the 28 days) and no rates.

## Step 5: The summary in chat

Short, plain words, at most about 250 words:

```markdown
## Your account, {YYYY-MM-DD} to {YYYY-MM-DD}

{One line: followers now, and against your last pull if there is one, with both values: "3,412 followers, up from 3,301 on 2026-11-07, +111."}

**Working, keep these:**
1. ...
2. ...
3. ...

**Not working, most important first:**
1. ...
2. ...
3. ...

**Fix this one first:** {the bottleneck in plain words, its one sum X ÷ Y = Z, and the page's "try this week" idea}.

**Your reels:** best {date, a few words}: score {N}; worst {date, a few words}: score {N} (each against your normal of {N} views, from the printout).

**Against your last pull:** {2 or 3 lines that moved most, each with the old value, the new value and the change: "Reach 18,240, up from 15,900 on 2026-11-07, +2,340". Or "This is your first pull. Pull again in a week to see what changed."}

{What Instagram didn't give, in one line: "Instagram didn't give your bio link taps this time, so that step says not given."}

Your full breakdown: `my-content-team/analytics/dashboard.html`
```

- Fewer than 3 in a list: write only what there is. Nothing on target: "Nothing is in its normal range yet." Never pad.
- One written sum in chat at most (house rules); the page has the rest.
- **A missing number is "not given", never 0**, in chat, in the files and in what you say about the page.
- **Fewer than 9 reels old enough** (the printout says "under 9"): say plainly, once, that the normal isn't reliable yet, with the count: "Your normal isn't reliable yet: 6 of the 9 reels it needs." No "winner" or "flop" anywhere. Say "did a lot better (or worse) than your others" only at about twice or about half the middle views, and call any pattern an early sign.
- **Every comparison shows both values** (old and new, or this post and the normal), never only the change.
- **Under 1,000 followers:** say once, plainly, that Instagram holds back some numbers for small accounts, which is why some cards say not given and reels are judged on likes. Never call it a problem with their account.
- **Benchmarks:** they are published averages, good for spotting a gap 5 times too big, not exact targets. "Reference accounts" on the page are two working accounts measured once, shown for reference only, never a goal. The comparison with their own last pull matters more. Say this once, the first time.
- **A 28 day figure is never "last week".** Say "in the last 28 days". Only the 7 day window is "last week".
- **The windows overlap:** pulls less than 28 days apart share days; when the printout says so, say "the change looks smaller than it is".
- **What the page can't see:** sales and bookings. If the goal is bookings or sales, the page has a box for page visits, sales and price: tell the owner they can type them in there to see the last two steps and what the fix is worth.

## Step 6: Update the files (existing rules)

- **`results-log.md`:** add the printout's rows to the Checks table (one row per reel per check, never change old rows). Swap the Post name for the plan's exact short name when the reel is in `content-plan.md` or has a card (match on date and first caption line; if it doesn't fit, follow Step 2 of the weekly report). Format and Hook type from the card first, else from `formats.md` marked guessed. Follows, Profile visits and Link taps stay `not given` (Instagram gives them for the whole account, not per reel). Add a line to "Account checks" with followers and the normal. Put the 28 day account sums the summary used under `## Working`. Fill "What's in each post" for new reels: "Where this came from" follows the card rules first (`from our card` or `from our card, not confirmed`); a reel with no card gets `Composio pull` (known numbers, guessed tags).
- **`performance-brief.md`:** only if the pull adds something the brief doesn't have yet (a new winner, a step that's clearly the bottleneck two pulls running). Same rules as the weekly report, Step 7: counts as evidence, strong or early sign, at most 7 rules.
- **`content-plan.md`:** a reel the plan lists that shows up in the pull is posted (weekly report, Step 8).
- `team-status.md`: the lines your work changed.

Then the checkpoint. Option 1, run alone: "Plan next week from this" (hands to the Content Strategist). In the Orchestrator's loop: the plain check-in.

## Without Composio

- **An export file (CSV):** the weekly report route is unchanged. If the owner also wants the page, run `python3 DASH --from-csv {file} --save-json my-content-team/analytics/{date}-instagram.json --today {date}`. An export has numbers for each post only, so the page shows the reels and says "no data" on the account steps; say so in one line ("For the funnel steps I need your account totals: connect Composio, or send a screenshot of your account Insights").
- **Screenshots or typed numbers:** the weekly report route. No page.
- Photo and carousel posts aren't on the page (it reads reels). The weekly report still counts them.

## Other platforms

What Composio has for TikTok, Facebook Pages, YouTube and LinkedIn, checked and unchecked: `composio-platforms.md`. Only Instagram has the full breakdown. For the others, use exports or screenshots (weekly report) unless that file says a pull is verified.
