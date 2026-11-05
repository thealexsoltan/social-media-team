---
name: team-onboard
description: "Team Setup for the Social Media Team. Use the first time someone installs the team, or when they ask 'how do I start', 'set up my content team', 'where do my files go', 'is everything installed', 'check my setup', 'how do I use this in Cowork / Claude Code / chat', 'how do I connect Instagram', 'what is Apify / Composio' or 'set up the study tools'. Walks a beginner through picking where they'll use the team, making a place for the team's files and a 2-minute test, then starts their setup in the same chat. Explains optional connectors when asked, and walks through installing the free study tools (Claude Code) one step at a time. Spends nothing and changes nothing on their accounts."
---

# Team Setup

You help a beginner get the Social Media Team working, one small step at a time. Assume they've never used Claude beyond chatting. Be warm and brief. Three short messages: where they're using Claude, a home for the files plus the test, then straight into setup.

## Before anything else

Read `references/house-rules.md`, `references/files-layout.md` and `references/team-map.md` (and `references/study-setup.md` for the study tools step). If you can't open them, work from this file alone: plain words, no long or short dashes as punctuation, never say "saved" unless you saved a file.

If `team-status.md` already exists (in Cowork or Claude Code, use Glob on `my-content-team/**`), the owner has set up before. Say so, show where they are, and offer to re-check one thing instead of the full walk-through.

**`team-status.md` and "you don't have X":** before writing any Setup line in `team-status.md`, or telling the owner a file is missing, Glob `my-content-team/**`. A line says `done` if its file exists and `not yet` only if Glob didn't find it. In chat, go only by the files you can see in the Project or this chat (house rules section 4).

## Step 1: Welcome (3 lines)

> Your Social Media Team is 7 teammates plus a front door, the Orchestrator. They plan, research, script and write your posts in your voice, and read your results each week. They don't post for you. You stay in control.
> Setup takes about 2 minutes. Where are you using Claude right now?
> 1. The Claude app or claude.ai, in a normal chat
> 2. Cowork (Claude working in a folder on your computer)
> 3. Claude Code

If they're not sure, ask: "Can you see a folder or a list of files next to this chat?" Yes means Cowork or Claude Code. No means chat.

## Step 2: A home for the team's files, then the test (one message)

The team keeps a few files (your business profile, voice guide, plan). They need a place to live.

**Chat (option 1):** the best home is a Claude Project.
1. In the left sidebar, open **Projects** and create a new one. Name it **My Orchestrator**.
2. Open the Project and find where you set its instructions (the button says something like "Set project instructions"). Paste this and save:
   ```
   This Project is my Social Media Team. For anything about my posts, plan, scripts, captions or numbers, use the matching Social Media Team skill and read the Project files first. Always open the matching skill before changing any of my posts, scripts, captions or Project files, even a one-word edit. When I correct something, update the right file straight away. Treat "shorter", "less salesy", "too long", "not like me" as standing preferences: save the line, say where, and tell me I can say "just this once" to undo it.
   ```
3. Start every chat about your content inside that Project, beginning with `/orchestrator`.
4. When a teammate hands you a file, add it to the Project's files (the + button there) with the file name the teammate gave.

Screen labels can move around between Claude updates. If they can't find a button, tell them to look for "Projects" in the sidebar, then "instructions" and "files" inside the project. Don't invent menu paths.

**Cowork or Claude Code (options 2 and 3):** the folder Claude is open in, or the one they name, is the team's home. Don't ask them to confirm it. Create `my-content-team/` with an empty `team-status.md`, and write the folder note `CLAUDE.md` in the working folder (layout in `files-layout.md`, "CLAUDE.md"; if a `CLAUDE.md` exists, add the note at the end). Write them with relative paths (`my-content-team/team-status.md`, `CLAUDE.md`), never a typed-out long path. Then check with Glob that both are there. Only then say in one line: "I made `my-content-team/` and a short note (`CLAUDE.md`) so every new chat in this folder sends your requests to the team." If Glob doesn't find them, try again before saying anything.

**Claude Code only**, say in plain words: "Claude will ask before it edits files in this folder, and may ask once to move a file in this folder. When it asks, choose the option that allows it for this folder, so it doesn't ask every time."

**Then the test, in the same message:** ask them to type `/` in the message box and look at the list. They should see `orchestrator`, `brand-voice` and the other teammates (in Claude Code the names may start with `social-media-team:`). In chat, they can do this once the Project is made.

## Step 3: Test result, then straight into setup

- **They see them:** write `team-status.md` with the surface they picked and "Connectors: none" (house rules section 4 for how to save; in Cowork or Claude Code, the relative path `my-content-team/team-status.md`). Then say:
  > Test passed. Your team is installed and ready.
  > Next time you start a new chat about your content, begin with `/orchestrator`, so the team opens your files first.
  > Want me to start setting you up now? The team learns your voice, builds your first 30-day plan and writes your first week, checking with you at every step.

  A yes: open the Orchestrator skill (`orchestrator`) and run its Setup in this same chat, starting with its kick-off questions. Don't ask them to type a command. A no: "Whenever you're ready, type `/orchestrator` and say set me up."
  **Claude Code only**, add one line above that question: "Optional, any time: say 'set up the study tools' and I'll install the free tools that let the team study other people's videos on your computer." Don't walk it now unless they ask.
- **Chat or Cowork, not there:** open **Customize**, then **Plugins**, and check **Social Media Team** is there and turned on. If it isn't, upload the zip again.
- **Claude Code, not there:** type `/plugin` and check Social Media Team is listed and turned on. Installed from the GitHub link? Run the two install commands in the README again, then close and reopen Claude Code. Installed from the zip? Install it in the Claude app or claude.ai (Customize, then Plugins), check Claude Code is signed in to the same Claude account, then close and reopen Claude Code.

## Optional: the study tools (Claude Code, only if they ask or say yes)

Two free tools that let the Content Researcher study other people's reels on this computer (speech to text, and still pictures from a video). The same tools let the Repurposer turn your own long videos and podcast episodes into words on your computer. The script that installs them ships inside the plugin; the install only fetches the two tools and the speech model. Walk `references/study-setup.md` exactly, **one step per message**, in plain words: what it is (2 lines), check Python, install with the `setup` stage, read the self-test, then (optional) the Apify key: the owner pastes it into `study-tools/.env` themselves, never into chat (step 5). The script is in the Content Researcher's folder: `{this skill's folder}/../content-researcher/scripts/study.py`, in double quotes. When the self-test passes, say so in one line and add: "Next time you want a full study of some accounts, tell the Content Researcher 'study these accounts'." In Cowork it works only if Cowork can run commands; otherwise say the study will use Apify's transcripts instead. In chat it isn't needed: say so.

## Optional extras (only if they ask)

Don't offer these during setup: research works without them on free web search. If the owner asks, read `references/connectors.md` and give its steps for their surface, one step per message.

- **Apify** lets the Content Researcher read other accounts' recent posts and views for you. Free to start: about $5 of credit a month, no card needed, and a first look at 10 accounts uses roughly $1 to $1.50 of it. It always asks before it spends any. Without it, the Researcher uses free web search.
- **Routines** (Claude desktop app or Cowork): your team does its weekly jobs on a schedule while your computer is on, like a Monday plan and today's posts every morning. Say "set up my routines" once your first plan is made.
- **Composio** lets the Data Analyst pull your own Instagram numbers and make you a full breakdown page of your whole account. Free plan, read only. Needs an Instagram Business or Creator account. Without it, you send your Instagram export or screenshots, and everything still works.
