# The 11 routines

Each routine is one scheduled task that opens one teammate in one mode, works only in `my-content-team/`, and leaves a line in `team-status.md` under `## Routines` saying what's waiting. Full card and the exact prompt for each: `routines/{slug}.md`. Paste the prompt exactly: it carries its own rules, because every run starts fresh with no memory.

## The list

| # | Routine | Teammate | Default (the computer's own time) | Cron | Needs |
|---|---|---|---|---|---|
| 1 | Monday Content Plan | Content Strategist | Mondays 7:00 am | `0 7 * * 1` | a first plan |
| 2 | Daily Post Drop | Copywriter | every day 8:00 am | `0 8 * * *` | a plan with dated rows |
| 3 | Wednesday Trend Scan | Content Researcher | Wednesdays 10:00 am | `0 10 * * 3` | a business profile |
| 4 | Friday Results Report | Data Analyst | Fridays 4:00 pm | `0 16 * * 5` | Composio for the full report, else it leaves a reminder |
| 5 | Monthly Plan Refresh | Content Strategist | the 1st, 3:00 pm | `0 15 1 * *` | a plan and an idea bank |
| 6 | Monday Kickoff | Orchestrator | Mondays 7:00 am | `0 7 * * 1` | setup finished |
| 7 | Filming Prep | Scriptwriter | the evening before filming day, 7:00 pm | `0 19 * * 6` (Sunday filming) | a filming weekday |
| 8 | New Long Piece Watch | Repurposer | Fridays 1:00 pm | `0 13 * * 5` | a source to watch |
| 9 | Monthly Voice Tune-up | Brand Voice | the 1st, 2:00 pm | `0 14 1 * *` | a voice guide |
| 10 | Monthly Re-study | Content Researcher | the 1st, 12:00 pm | `0 12 1 * *` | study tools, an Apify budget, Keep accounts |
| 11 | Monthly Review | Data Analyst | the 1st, 11:00 am | `0 11 1 * *` | 4 weeks of results |

One line each, for the owner (use these words in Set up):
1. **Monday Content Plan:** plans your week every Monday morning.
2. **Daily Post Drop:** writes today's posts every morning, ready for you to check and paste.
3. **Wednesday Trend Scan:** checks what's new in your niche every Wednesday.
4. **Friday Results Report:** reads your week's numbers every Friday and says what to post next (needs Composio, or it reminds you to send them).
5. **Monthly Plan Refresh:** on the 1st, adds last month's lessons to your ideas and keeps 4 weeks planned ahead.
6. **Monday Kickoff:** the whole week every Monday: plan, filming cards and captions. Pick this or Monday Content Plan, not both.
7. **Filming Prep:** the evening before you film, writes the filming cards for tomorrow.
8. **New Long Piece Watch:** on Fridays, checks your YouTube, podcast or blog for something new and turns it into 10 pieces.
9. **Monthly Voice Tune-up:** on the 1st, suggests changes to your voice guide. Changes nothing without your yes.
10. **Monthly Re-study:** on the 1st, studies the accounts you learn from again, within an Apify budget you set (Desktop app's Code tab or Claude Code only).
11. **Monthly Review:** on the 1st, a longer look at last month's results.

**Starter set** (what to turn on when the owner says "you pick"): Monday Content Plan, Daily Post Drop, Wednesday Trend Scan, Friday Results Report and Monthly Review. Add Filming Prep if the owner has a filming weekday. None of these spends anything.

## Why the times are spread out

Two runs at the same time could both edit `team-status.md` or the plan. So:
- Mornings: Monday plan 7:00, Daily Post Drop 8:00 (Monday's posts exist before it runs), Wednesday scan 10:00.
- Fridays: New Long Piece Watch 1:00 pm, Friday Results Report 4:00 pm.
- The 1st: Monthly Review 11:00 am (fresh brief first), Monthly Re-study 12:00 pm, Monthly Voice Tune-up 2:00 pm, Monthly Plan Refresh 3:00 pm (last, so it plans from the freshest files). Even when the 1st is a Monday, Wednesday or Friday, nothing lands in the same hour.
- Filming Prep: 7:00 pm, clear of everything.

If the owner moves a time, keep it at least an hour from the others on the same day, and keep the monthly order. Desktop scheduled tasks also start a few minutes late on purpose (to spread the load), so never set two in the same hour.

## Monday: one plan, never two

Monday Content Plan and Monday Kickoff both make this week's plan. The Kickoff also writes the filming cards and captions. The owner turns on one or the other:
- Set up never offers both as on. If the owner picks both, ask which one, in one line: "Both make your Monday plan. Kickoff also writes your cards and captions. Which one?"
- Each prompt also checks `## Routines` and stops if the other one is listed as on.
- Both prompts update a week that already exists instead of adding a second copy, and Daily Post Drop never rewrites a post that already has its file.

## The monthly ones run once a month, whatever the trigger

Each monthly prompt starts with a check: if the run log already has its line this month, it stops. That keeps a catch-up run from doing the job twice, and lets Cowork (which has no monthly option) run them on a weekly trigger: the first run each month does the work, the rest stop at once.

## What it costs

- Each run is a Claude session on the owner's plan and uses their Claude usage like a chat would. Daily Post Drop is about 30 runs a month, the busiest one. Say this once in Set up.
- Apify only in Monthly Re-study and New Long Piece Watch (YouTube captions, about half a cent). Both stay inside `Apify budget a month` in `team-status.md`. With no budget line, or $0, they never pull.
- Composio (Friday Results Report) is free and read only.

## Values that live in team-status.md, not in the prompts

The prompts are the same for every owner. Everything that's the owner's own lives in the `## Routines` section of `team-status.md` (layout in `files-layout.md`): which routines are on, the filming days for Filming Prep, the Apify budget and what's used, watched sources, the Re-study accounts and reel count. To change one of these, Edit that line: the task itself doesn't change. Only a time or a filming day changes the task's schedule.
