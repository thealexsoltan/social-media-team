<!-- Copied from shared/team-map.md by scripts/sync-shared.mjs. Edit the shared file, not this copy. -->
# Team map

## Who does what

| Teammate | Type | Main jobs | Needs | Makes |
|---|---|---|---|---|
| **Orchestrator** | `/orchestrator` | Front door, setup, weekly loop, status, anything about posts, plan, scripts, captions or numbers that isn't clearly one teammate's job | anything | `team-status.md` |
| **Brand Voice** | `/brand-voice` | Business profile, voice guide, voice checks, saving corrections | the owner's own posts, emails or a voice note | `business-profile.md`, `voice-guide.md`, `learned-rules.md` |
| **Content Researcher** | `/content-researcher` | 10 accounts to learn from, qualify an account, study their winners, what's new in the niche, a full study of 2 to 5 accounts with script templates (Claude Code best) | account names, or "you pick". It looks accounts up on the web for free. Apify or grid screenshots add checked numbers, only if the owner wants them | `competitors.md`, `research-notes.md`, `study/`, `script-templates.md` |
| **Content Strategist** | `/content-strategist` | a content matrix (your topics × 8 post styles, 40 to 56 ideas), 30-day plan picked from it, next week's plan, 1 idea into 5 angles or 3 per square | profile, research, results if any | `idea-bank.md`, `content-plan.md` |
| **Scriptwriter** | `/scriptwriter` | Filming cards with the four hooks, hooks only, 3 videos from 1 shoot | voice guide, plan | `scripts/` |
| **Copywriter** | `/copywriter` | Caption packs (with the video's text on screen and first frame), posts, carousels, headlines, the week's text. Uses the study's winning caption shapes and the script templates when they exist | voice guide, plan or a script | `posts/` |
| **Repurposer** | `/repurposer` | 1 long piece into 10 (or the number the owner picks), filled into the script templates | the long piece: the owner's own or someone else's video, podcast, blog, newsletter, or a research paper (a link, a file or the text) | `repurposed/` (plus `scripts/` and `posts/` for rows it adds) |
| **Data Analyst** | `/data-analyst` | Full account breakdown (a dashboard page from a read only Composio pull), weekly report, why a post flopped, monthly review, the performance brief | Composio connected, or the owner's numbers (paste, export or screenshots) | `results-log.md`, `performance-brief.md`, `analytics/` |
| **Team Routines** | `/team-routines` | Sets up, changes and lists the routines: scheduled tasks that run one teammate on a schedule in the owner's content folder (Monday plan, today's posts every morning, Wednesday trend scan, Friday report and 7 more). Desktop app or Cowork only | `my-content-team/` set up, the owner's yes to each task | scheduled tasks on the owner's computer, the `## Routines` section of `team-status.md` |
| **Team Help** | `/team-help` | Questions about the team, fixing problems, "where am I" | nothing | nothing |
| **Team Setup** | `/team-onboard` | First-time setup on any Claude surface | nothing | `team-status.md` |

## The plan's status steps

`idea` > `scripted` (Scriptwriter) > `filming` (the owner) > `ready` (Copywriter, once the video is filmed) > `posted` (Data Analyst, or the owner). Only the Strategist adds or moves rows; the Repurposer may add rows.

## Routing small requests

| The owner says something like... | Send to |
|---|---|
| "learn my voice", "make this sound like me", "never say X", "dont call it X", "I say X not Y", "that's not how I talk" | Brand Voice (saves the rule the same turn) |
| "who should I copy?", "is this account any good?", "what's trending in my niche?", "study these accounts", "make me script templates" | Content Researcher |
| "what should I post?", "give me ideas", "content matrix", "plan my month", "cant film monday, move stuff", "fewer videos" | Content Strategist |
| "write a script", "give me hooks", "what do I say in this video?", "script from template 3" | Scriptwriter |
| "write a caption", "write a post", "write my posts for the week", "make it shorter", "less salesy" (about a caption), "what text goes on screen", "first frame idea" (for a video that already has its script) | Copywriter (and a line in `learned-rules.md`) |
| "turn this video/podcast/blog into posts", "turn this into some posts", "turn this YouTube video into reels", "make posts from this research paper / PDF" | Repurposer |
| "break down my account", "pull my numbers", "refresh my dashboard" | Data Analyst (Full account breakdown) |
| "how did my posts do?", "why did this flop?", "here are my numbers" | Data Analyst. If it's last week's numbers and `content-plan.md` exists, it's the Orchestrator's **weekly loop**: the Data Analyst goes first and option 1 carries on to next week's plan, scripts and captions |
| "set up my routines", "routines", "run this every Monday", "pause my Friday report", "change my post drop time", "what routines do I have", "did my routine run" | Team Routines |
| "what's waiting?", "what did the routines make?" | Orchestrator (reads "Waiting for you" in `team-status.md`) |
| "how does this work?", "something went wrong" | Team Help |
| anything else about the owner's posts, plan, scripts, captions or numbers | Orchestrator |

## If a teammate is missing

On claude.ai and Cowork the team comes as one plugin. If a teammate's skill can't be found, the owner probably uploaded only part of it. Tell them: "Open Customize, then Plugins, and check Social Media Team is installed and turned on. If it is, upload the zip again and choose Replace." Then carry on with what's available.
