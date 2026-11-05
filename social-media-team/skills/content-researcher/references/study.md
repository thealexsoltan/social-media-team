# Study accounts: a full reel study, then templates

The deepest research the team does. For 2 to 5 accounts the owner likes: every recent post's numbers, then the best reels taken apart second by second (what's said, what's on screen, how it's cut), a playbook of what's working, and fill-in-the-blank script templates built from the winners.

## What it makes

All in `my-content-team/study/` (layouts in `files-layout.md`, "study/ folder"), plus `my-content-team/script-templates.md`:

| File | Made by |
|---|---|
| `study/{handle}/stats.md` | the study script |
| `study/dashboard.html` (every account, a sortable table of every post) | the study script |
| `study/{handle}/transcripts/`, `study/{handle}/frames/` | the study script |
| `study/{handle}/breakdowns/{code}.md` | the script makes a stub with the facts, you fill it in |
| `study/playbook.md` | you |
| `script-templates.md` | you |
| short version in `research-notes.md` and the rows in `competitors.md` | you |

## Where it runs

| Surface | What works |
|---|---|
| Claude Code | Everything |
| Cowork (folder open) | Everything, if Cowork can run the script and download. If a step can't, use the chat route for that step |
| claude.ai chat | Numbers from the pull (you work them out with `outlier-score.md`), spoken words from Apify's transcripts, breakdowns from the words, playbook, templates. **No frames and no pacing.** Say so once: "In chat I can't download videos, so I'll work from the words: no pictures and no cut counts." |

It needs an Apify account (`connectors.md`): either the owner's Apify key saved on this computer (the `pull` stage, best in Claude Code) or the Apify connector. Apify off or declined? Don't push it (rule 1). Offer the screenshot route (Study winners) instead.

## The script

`scripts/study.py` in this skill's folder. Claude Code shows the folder when this skill opens. Below, `STUDY` means that full path in double quotes, like `"/path/to/content-researcher/scripts/study.py"`.

- Run it from the owner's working folder (the one with `my-content-team/` in it). One command at a time, never chained.
- It's the **one** tool allowed to write inside `my-content-team/` (only into `study/`). Everything else you change with Read, Write and Edit as usual.
- Videos and pulls go to `study-tmp/` next to `my-content-team/`, never inside it.
- Tell the owner once: "Claude may ask you to allow a few commands while I work, that's normal."
- Windows: `python` instead of `python3`.
- First time? `python3 STUDY selftest`. If it says the tools aren't installed, walk the owner through `study-setup.md` first (one step per message), then come back. Don't install anything without telling them what it is.

## The steps

### 1. Ask for the accounts

> Send me 2 to 5 accounts whose content you like (handles or links). Add your own handle if you want me to compare.

Skip it if the owner already named them, or `competitors.md` has Keep rows (offer those: "I'll study your 3 kept accounts: @a, @b, @c. Want to swap any?"). Run by the Orchestrator, use what its kick-off got. Look each handle up on the web first (rule 2). Instagram and TikTok only; other platforms get the screenshot route.

### 2. How many reels: check the plan

Each reel you study uses a good share of the owner's Claude usage, so the owner picks the number.

- **Claude Code:** run `python3 STUDY plan`. It reads only 2 lines from Claude's own settings file and prints them, plus a suggestion. Never read or print anything else from that file.
- **No answer from it, or not Claude Code:** ask: "Which Claude plan are you on: Pro, Max 5x, Max 20x, or something else?"
- Recommend: **Pro: 5 to 6 reels. Max 5x: 10. Max 20x or higher: 15.** Not sure: 5.
- Always add: "15 is the most I'd do in one go. You can ask for more, it just uses more of your Claude usage."
- The owner's number wins, higher too. Ask this in the same message as step 3's yes, so it's one question.

### 3. Pull the posts (yes and cost first)

Per account: the last 30 posts, plus the follower count. **Use only the Actors (Apify's tools) in `apify-actors.md`**; anything else follows the rule at the top of that file, with the owner's yes. For a study:
- **Instagram:** `apify/instagram-reel-scraper` (30 reels; views only exist on reels), plus `apify/instagram-profile-scraper` for the follower count only.
- **TikTok:** `clockworks/tiktok-profile-scraper` (30 posts, with the video links). Followers come with it.

**Big creators** (100,000+ followers, or under 5 winners in their 30) get one longer pull, up to a year (250 posts), so there are enough winners to study. Put it in the same yes, so nobody is asked twice:

> I'll pull the last 30 reels from @a, @b and @c on Instagram, plus their follower counts: about 30 cents of your free Apify credit. If one of them turns out big or has fewer than 5 standouts, I'll go back up to a year (250 reels) for that one, about 70 cents more. And I'd study 6 reels in all (you're on Pro). Go ahead?

**Instagram shares** are a paid add-on that works only on a paid Apify plan (`check-apify` says which plan the owner has). On a paid plan, put them in the same yes with both prices: "Share counts too: about 21 cents more for 30 reels per account (on by default). For the year pull they're off unless you want them: about $1.75 more per account." On the free plan, leave shares out (the script does too) and Instagram shares stay `not in the public data`.

Costs (Apify's free plan prices, checked 2026-11-04, `apify-actors.md`): Instagram about 9 cents per 30 reels (about 65 cents per 250), plus about a quarter of a cent per follower count; share counts (paid plans only) about 21 cents more per 30 reels. TikTok about 13 cents per 30 videos with the video links (about $1.08 per 250). Round up when you quote.

**Two ways to pull. Use the first one that works:**

**A. From this computer (Claude Code, or Cowork that can run commands), with the owner's Apify key in `study-tools/.env`.** Cheapest on Claude usage, because the posts go straight into files and never pass through the chat.
- No key yet? Walk `study-setup.md` step 5 (the owner pastes the key into the file themselves; never ask for it in chat, never put it in a command, never read the file). `python3 STUDY check-apify` confirms it.
- After the owner's yes, run: `python3 STUDY pull --instagram handle1,handle2 --tiktok handle3 --posts 30 --budget 0.50` (Instagram shares are on by default for 30 reels and off for a year pull; add `--shares` or `--no-shares` to match the owner's yes. On a free Apify plan the script leaves them out by itself) (`--budget` = the spending cap in dollars: a little above your quote, never above what the owner agreed to). It runs one Actor per account plus the follower counts, waits, and saves each into `study-tmp/pulls/` in the shape `stats` reads. It prints what each run cost, from Apify.
- The year pull for a big creator: the same command with `--posts 250` and only that handle. It asks Apify for up to 250 posts or one year back, whichever comes first, and replaces that account's file. If fewer come back, the script says how many and how far back: tell the owner in one line, never fill the gap.
- The script checks the owner's Apify credit first. Apify quietly lowers a run's spending cap to the credit left this month, which cuts a pull short; the script warns before and says so after. Credit used up: it stops, and you use the message in `connectors.md`.
- Say what it cost in one line, from the script's output (`Apify cost this pull`).

**B. Through the Apify connector** (no key on this computer, or chat). Run the same Actors through the connector, then **save each pull as a file**, exactly as Apify returned it (a JSON list), with Write:
- `study-tmp/pulls/{handle}.json` for the posts, `study-tmp/pulls/{handle}-profile.json` for the profile. A longer pull for the same account gets its own file (`{handle}-year.json`); the script merges them.
- Keep it small: ask the dataset tool for these fields only.
  - Instagram: `shortCode, url, type, timestamp, videoPlayCount, videoViewCount, likesCount, commentsCount, videoDuration, caption, isPinned, ownerUsername, inputUrl, videoUrl, audioUrl, displayUrl, musicInfo` (profile: `username, followersCount`).
  - TikTok: `id, text, createTimeISO, playCount, diggCount, commentCount, shareCount, collectCount, videoMeta, webVideoUrl, mediaUrls, isPinned, isSlideshow, authorMeta, musicMeta`.
- Set the run's spending limit a little above the estimate. Writing a 250-post pull out by hand uses a lot of Claude usage: if the owner wants year pulls often, suggest route A once.

Either way: video links stop working after 1 to 3 days, so download the same day.

### 4. Account numbers

Run `python3 STUDY stats` (add `--today YYYY-MM-DD` when the owner gave today's date; add `--followers handle=12345` when the owner told you a follower count the pull didn't have). Stats saves the date and every account's normal in `study-tmp/study-state.json`; every later stage reads them, so the numbers in the stubs always match `stats.md`. Pass `--today` to stats only. If the pulls change (a new pull), run stats again before anything else: the script says so.

It writes `study/{handle}/stats.md` and `study/dashboard.html`, no Claude work needed: followers, posts pulled, dates, posts per week, the normal (middle views, pinned posts and posts under 3 days old left out, newest 30 videos), reach, likes and comments per 1,000 views, shares and saves (TikTok only; Instagram says `not in the public data`, because the public post data has no share or save count), middle length, best posting days, every post's score, winners and the top 10.

Then:
- **Instagram shares and saves:** shares are in `stats.md` only when the shares add-on was pulled (paid Apify plans). When they weren't, they're `not in the public data`: never guess or rank which Instagram post was shared or saved most, not even as a best guess, and offer the score, likes or comments instead. Instagram saves are never in the public data.
- Show a short summary in chat: one line per account (normal, reach, winners, the best 2 or 3 with scores), marked `Apify`, and "the full numbers are in `study/{handle}/stats.md`; open `study/dashboard.html` to sort every post".
- Add or update each account's row in `competitors.md` from these numbers, with the Qualify rules (verdict check included). Don't run a separate qualify.
- Big creator rule from step 3: if an account has 100,000+ followers or under 5 winners and the owner's yes covered it, pull the year now, save it, run `stats` again.
- Never retype a number from memory. Copy it from `stats.md`.

### 5. Pick the reels

Run `python3 STUDY pick --total N` (N = the agreed number). It takes the top winners (2.0 or more of their own normal), taking turns between accounts, plus 1 or 2 normal posts per account for contrast, counted inside N. An account with no single winner gives its best videos instead.

Show the list in one short block: account, date, views, score, and the topic in a few plain words from the caption. Then **stop and ask**, as a short check-in, so the owner sees what will be studied before it's studied:

> These 6, go? Or tell me which to swap.

Wait for the answer. Skip the wait only if the owner already said "you pick" (or "just do it") for the reels, or the Orchestrator runs you: then carry on and show the list in the final reply. To change it: `python3 STUDY pick --codes CODE1,CODE2,...` (codes are in `stats.md`). If the script says there are fewer winners than asked for, say so in one line.

### 6. Download, words, pictures

Run these one at a time, each when the last one is done:

1. `python3 STUDY download`: the picked videos into `study-tmp/videos/`. A link that has expired: pull that account again (`pull`, or the connector), `stats`, then `download`.
2. `python3 STUDY transcribe`: the words with times, on this computer, free. Music-only reels come out as `[no speech]`. The default speech model is small and quick; add `--model small.en` for harder accents (slower).
3. `python3 STUDY frames`: still pictures every half second for the first 3 seconds (`hook.jpg`), one picture per second after that (`seconds-1.jpg` and on, 24 to a sheet), and the cuts (how often the picture changes).
4. `python3 STUDY stubs`: one breakdown file per reel, the measured facts already in it.

Rough time on a recent computer: a few seconds per reel for each of transcribe and frames (rough guess, older computers are slower). A step that fails falls back for that step only (table below).

### 7. Break down each reel

For each stub in `study/{handle}/breakdowns/`: read the stub, then `hook.jpg` and **every** `seconds-*.jpg` it lists. Fill it in with Edit, following `study-breakdown.md`, and set `status: done`. 300 to 500 words each, tables included (a hard limit: count before saving). Facts only from the stub and the pictures. A contrast post gets the same treatment: what it did differently is the lesson.

Many reels? Do them in order and keep going; don't stop for a check-in between reels.

### 8. The playbook

Write `study/playbook.md` (layout in `study-breakdown.md`): what's working across the accounts and why, each line counted "x of y reels". Then the short version into `research-notes.md` (layout in `research-files.md`):
- one "Top hooks" entry per winner studied, its four hooks taken from the breakdown, `Seen from: Study accounts (video still, machine heard on this computer, music info)`;
- "Formats that win", "Hook types that win" and "Topics that win" counted from the breakdowns;
- refresh the Competitor Brief's "In short" if this changes it. Keep everything else in the file.

### 9. Templates

Write `script-templates.md`: one template per winning reel (not the contrast posts). How: `writing-templates.md`. Layout: `files-layout.md`.

### 10. Clean up, check in, hand off

1. `python3 STUDY cleanup` deletes the downloaded videos only (they're other people's). Say so in one line. The pulls stay in `study-tmp/pulls/` by default, so the numbers can be re-run later. `cleanup --all` deletes them too, only if the owner asks.
2. Update `team-status.md` ("Competitors and research: done").
3. Reply, **short** (about 250 words, never more than 350). Everything else stays in the files. In this order:
   - the numbers in **3 lines** at most (normal, reach, winners, Apify cost),
   - the **top 5** playbook points, one line each with its count,
   - the templates, **one line each** (number, name, best for),
   - the files saved, one line each (folders as one line: `study/{handle}/breakdowns/ (6 reels)`),
   - the hand-off line and the checkpoint.
   Don't repeat the reel list (the owner saw it at step 5) or explain the method.
4. Hand-offs (run on your own): "Brand Voice can build your style guide from these breakdowns: type /brand-voice and say 'build from winners'. The Scriptwriter can write from any template: type /scriptwriter and say 'script from template 2 about {a topic of yours}'. The Repurposer can fill these templates from any long video, podcast or paper: type /repurposer." Run by the Orchestrator: name the teammates, no commands.
5. One checkpoint at the end of the whole study (house rules section 5). The only stops before it: the yes in step 3 and the reel list in step 5.

## If a step fails

Say what happened in one line, fall back for that step only, and keep going.

| Problem | Fallback |
|---|---|
| Tools not installed and the owner says no, or setup fails | The chat route for steps 6 and 7: spoken words from Apify (Instagram: the reel scraper's transcript add-on, about 5 cents a minute of sound; TikTok: its own captions, free; `invideoiq/video-transcriber` only as the last resort, `apify-actors.md`), no frames, no cuts. Ask yes and cost first |
| `stats` says no pulls found | Check the files are in `study-tmp/pulls/` and end in `.json` |
| A download fails (link expired) | Pull that account again (`pull`, or the connector), `stats`, `download` |
| `pull` says the key is missing or wasn't accepted | `study-setup.md` step 5. Meanwhile, route B (the connector) works |
| `pull` saved fewer posts than asked | The spending cap was reached, or the account has fewer posts. Say so; go on with what came |
| Cowork can't download or run commands | "Cowork couldn't run the study tools here. You can allow more in Claude's Settings, under Capabilities." Then the chat route |
| A reel is private or deleted | Skip it, say which |
| A transcript looks wrong (a word that makes no sense) | Trust the words burned into the video when the pictures show them, and say so in the breakdown |
| Apify credit used up | The message in `connectors.md`, then screenshots |

## The chat route, start to end

1. Steps 1 to 3 the same, but ask which plan (no script). In chat also add the transcripts to the yes: the Instagram reel scraper's transcript add-on (about 5 cents a minute of sound), free for TikTok captions.
2. Work out the numbers yourself from the pull (`outlier-score.md`), for each account the same lines as `stats.md` (layout in `files-layout.md`), and hand them over as file blocks named `study-{handle}-stats.md`. No dashboard.
3. Pick the reels the same way (winners taking turns, 1 or 2 normal posts per account).
4. Get the words (TikTok captions, Apify transcript). Break each reel down from the words, the caption and the numbers only: sections that need pictures just say `not seen`. The one explanation (no pictures in chat) is given once, at the start; don't repeat why in the reply, the breakdowns or the playbook.
5. Playbook, templates and research notes the same, as file blocks (`study-playbook.md`, `script-templates.md`, `research-notes.md`), with the keep-it steps from house rules section 4. In chat nothing is saved by you: never write "I've added", "saved", "logged" or "updated". Give the file block and say "add this to your Project" (or the copy-paste line).

## Adding accounts later

New accounts: pull, save, `stats` (all accounts stay in the dashboard), `pick --codes` for the new reels only, then steps 6 to 10. Add the new templates at the end of `script-templates.md` with the next numbers; never renumber old ones, because the Scriptwriter may have named them.
