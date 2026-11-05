# Social Media Team

Your AI social media team, inside Claude: seven teammates and a front door who learn your voice, plan your month, write your video scripts and captions, and read your results every week.

They don't post for you. You stay in control. You need a paid Claude plan (Pro or above), and nothing else to pay for.

## Install in the Claude desktop app

No terminal needed.

1. Open the Claude desktop app and go to the **Code** tab.
2. Click the **+** next to the message box, then **Plugins**, then **Browse plugins**.
3. Click **Add** at the top right, then **Add marketplace**, then **Add from a repository**.
4. Paste this link and click **Sync**:

```
https://github.com/thealexsoltan/social-media-team
```

5. Find **Social Media Team** in the list and install it.
6. Start a new chat and type:

```
/team-onboard
```

## Install from a terminal instead

Only if you use Claude Code in Terminal (Mac) or PowerShell (Windows). Run these yourself, not inside Claude. Paste one line at a time.

```bash
claude plugin marketplace add thealexsoltan/social-media-team
```

```bash
claude plugin install social-media-team@viral-skool
```

On Windows this needs [Git for Windows](https://git-scm.com/downloads) installed first.

Then open Claude Code in the folder you want to keep your content in, and type `/team-onboard`.

## What setup does

`/team-onboard` takes about 2 minutes and spends nothing.

1. It asks where you're using Claude.
2. It makes a folder called `my-content-team` (where your business profile, voice guide and plans live) and a short note called `CLAUDE.md`, so every new chat in that folder goes to the team. Claude asks before it edits files there: choose the option that allows it for this folder, so it doesn't ask every time.
3. It runs a quick test: type `/` and you should see the teammates in the list.
4. Then it offers to start your setup straight away. The team learns your voice, builds your first 30 day plan and writes your first week of scripts and captions, checking with you after every step.

Optional, any time:

- Say **set up the study tools** to install two free tools that let the team study other people's reels on your computer (about 400 MB, a few minutes, once).
- Connect **Apify** (free to start, no card) so the team can read other accounts' posts and views for you. It always asks before it spends any of your free credit. Without it, you send screenshots instead.
- Connect **Composio** (free plan, read only) so the Data Analyst can pull your own Instagram numbers. Without it, you send your Instagram export or screenshots.

Every time you start a new chat about your content, begin with `/orchestrator` (or a teammate's command, like `/copywriter`), so the team opens your files first.

## The team

| Type | Teammate | What it does |
|---|---|---|
| `/orchestrator` | Orchestrator | Your front door. Runs setup and your weekly content in order |
| `/brand-voice` | Brand Voice | Learns how you talk and write, and keeps every post sounding like you |
| `/content-researcher` | Content Researcher | Finds accounts in your niche that keep going viral and studies their best posts |
| `/content-strategist` | Content Strategist | A content matrix of 40 to 56 ideas (your topics × 8 post styles) and a 30 day plan picked from it, with a short brief for every post |
| `/scriptwriter` | Scriptwriter | Video scripts: what to say and what to show, with a strong hook |
| `/copywriter` | Copywriter | Captions and posts for every platform, ready to paste |
| `/repurposer` | Repurposer | Turns one long video, podcast or blog into 10 pieces |
| `/data-analyst` | Data Analyst | A full breakdown of your Instagram account in one page, plus a plain English weekly report: what worked, what flopped, what to post next |
| `/team-routines` | Team Routines | Sets up your routines: the team's weekly jobs on a schedule (a Monday plan, today's posts every morning, a Friday report and more). Runs in the Claude desktop app or Cowork while your computer is on, and never posts for you |
| `/team-help` | Team Help | Questions and fixes |
| `/team-onboard` | Team Setup | First time setup |

In Claude Code the commands can show up with the plugin's name in front, like `social-media-team:orchestrator`. Both work.

## Using Claude chat, claude.ai or Cowork

The install above is for the Code tab and Claude Code. To use the team in a normal Claude chat, on claude.ai or in Cowork, install the zip that came with your purchase instead:

1. Open **Customize**, then **Plugins**.
2. Choose **Add**, then **Upload plugin**, and pick `social-media-team.zip`.
3. Start a new chat and type `/team-onboard`.

To update the zip later, upload the new one the same way and choose **Replace**.

Using chat or Cowork? For the Data Analyst's account breakdown page, open `dashboard.html` (in this repo, or the file that came with your purchase) in your browser, press paste instead, and paste the block the Data Analyst gives you.

## Getting updates

Fixes and new skills arrive as updates to this plugin. Your own files in `my-content-team` stay exactly as they are.

**The easy way:** when there's a new version, Claude tells you and asks if you want it. Say yes. You can also say this in any chat, any time:

```
update the team
```

**From a terminal instead:** paste one line at a time.

```bash
claude plugin marketplace update viral-skool
```

```bash
claude plugin update social-media-team@viral-skool
```

After an update, start a new chat so Claude loads the new version (in Terminal, close Claude Code and open it again).

## Help

Type `/team-help` for questions and quick fixes. Still stuck? Email hello@viralskool.ai. Say what you were doing and what happened. A screenshot helps.

---

© Viral Skool. For buyers of the Social Media Team, under the terms you agreed to at purchase. Not affiliated with or endorsed by Anthropic or Instagram.
