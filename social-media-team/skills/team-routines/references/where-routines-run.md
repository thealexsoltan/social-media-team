# Where routines can run

Checked against Anthropic's own pages on 2026-11-04. Screen labels move between Claude updates: if the owner can't find a button, tell them to look for "Scheduled", never invent a menu path.

## The Claude desktop app (the Code tab): the main route

Source: https://code.claude.com/docs/en/desktop-scheduled-tasks.md

- A local scheduled task runs on the owner's computer, in a folder they choose, with access to the files there. That's why it can work in `my-content-team/`.
- **It runs only while the app is open and the computer is awake.** If a run is missed, the app does one catch-up run when the computer wakes, for misses in the last 7 days.
- **Keep computer awake** is a setting in the app's Settings. With it on, overnight runs happen as long as the computer stays on and plugged in.
- The schedule is a cron line in the computer's local time. Runs start a few minutes late on purpose, to spread the load.
- Each task has its own permission mode. **A run that needs a tool the owner hasn't approved waits** in that run's session until someone answers. That's why Set up does one "Run now" per task while the owner is there: they approve the prompts once (choose the option that allows it for this folder), and later runs don't stop.
- Each run is a session. The owner finds them in the Code tab under **Scheduled**, then the task, then its runs (History).
- In a desktop session, Claude can create the task itself with the scheduled-tasks tools (create, list, update, run, delete). The owner can also make one by hand: Code tab, **Scheduled**, new task.

**Not checked (say so if it matters):** the create tool has no folder field. A task made from a chat seems to use that chat's folder, so Set up runs only in a session opened in the owner's content folder, and asks the owner to check the folder shown on each task in **Scheduled**. The permission mode isn't set by the tool either: the owner checks or changes it on the task.

## Cowork: the second route

Source: https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork

- All paid plans. In the sidebar, **Scheduled**, then **New task**. Two ways: **Create with Claude**, or **Set up manually**: name, prompt, approval mode, frequency, an optional model, an optional folder.
- Frequencies: hourly, daily, weekly, weekdays, or manual. **There's no monthly option**, so the monthly routines use Weekly on Monday: their prompts do the work on the first run each month and stop on the rest.
- Pick the owner's content folder (the one holding `my-content-team/`) as the folder.
- Approval mode: the safest is the one that asks first. Then a run may wait for the owner's OK, so do one manual run while they're there. (The exact labels weren't checked: read them off the screen.)
- Cowork runs on the owner's computer, so the same rule applies: Claude has to be open and the computer awake. (Inferred from it working in a local folder; not stated on that page.)
- Monthly Re-study isn't offered in Cowork: it needs the study tools, which run from the Code tab or Claude Code.

## Cloud scheduled tasks: not used

`/schedule` (it used to be called "routines" in Claude Code) runs in the cloud. It can't reach the owner's local files, so it can't read or write `my-content-team/`. Never set the team's routines up there, even though the name is the same.

## Claude Code in a terminal

There's no lasting schedule from a plain terminal session. `/loop` repeats a prompt only while that session stays open, and it expires. For routines that keep running, the owner needs the Claude desktop app (Code tab, Scheduled) or Cowork. Same folder, same plugin.

## Claude chat or claude.ai

No local scheduled tasks, and a Project's files can't be reached by a schedule. Routines need the desktop app or Cowork with the team's files in a folder.

## Plugins can't ship tasks

No field in a plugin's files creates a scheduled task. Team Routines makes them in the owner's own session, one by one, only after the owner says yes to each.
