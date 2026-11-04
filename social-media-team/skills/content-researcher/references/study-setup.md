<!-- Copied from shared/methods/study-setup.md by scripts/sync-shared.mjs. Edit the shared file, not this copy. -->
# Study tools: the one-time install

The study tools turn other people's videos into text and still pictures **on the owner's own computer**. Free, no account, no key. Nothing leaves the computer except the Apify pull. They come inside the team's plugin, in the Content Researcher's folder: `scripts/study.py` and `scripts/requirements.txt`.

Needed for **Study accounts** in Claude Code (and in Cowork, if Cowork can run commands). Not needed in claude.ai chat: chat uses Apify's transcripts instead, with no pictures.

## Finding the script

When a skill opens, Claude Code shows that skill's folder (the "base directory"). The script is at:
- From the Content Researcher: `{its folder}/scripts/study.py`
- From Team Setup: `{its folder}/../content-researcher/scripts/study.py`

Always put the whole path in double quotes (folder names can have spaces). Below, `STUDY` stands for that quoted path. Run every command from the owner's working folder (the one with `my-content-team/` in it), one command at a time, never chained with `&&` or `;`.

## Walk the owner through it

One step per message. Plain words. Wait for each step to finish before the next.

**1. Say what it is, in 2 lines.**
> To study videos properly I need two free tools on your computer: one turns speech into text, one cuts still pictures from a video. Everything you need is already in the team's folder, we're just installing it. It runs on your computer, so nothing leaves it except the Apify pull. About 400 MB in all, a few minutes, once.

**2. Check Python.** Run `python3 --version` (Windows: `python --version`).
- `Python 3.9` or newer: go on.
- Missing, or older than 3.9:
  - **Mac:** running `python3` the first time may pop up "install the command line developer tools". Tell the owner to click **Install** and wait for it to finish (a few minutes), then try again. Or install Python from python.org (the big yellow Download button).
  - **Windows:** install Python from python.org. On the first screen of the installer, tick **Add python.exe to PATH**, then **Install Now**. Close and reopen Claude Code afterwards.
  - Don't go on until `--version` shows 3.9 or newer.

**3. Install.** Run `python3 STUDY setup` (Windows: `python STUDY setup`). It:
- makes a private tools folder called `study-tools` in the owner's home folder (so nothing else on the computer changes),
- installs faster-whisper (speech to text) and imageio-ffmpeg (the video tool) from `requirements.txt` (about 260 MB),
- runs the self-test, which downloads the speech model the first time (about 150 MB).

Tell the owner: "This takes a few minutes. Claude may ask you to allow the command, that's normal."

**4. Read the self-test.** The last line says `Self-test passed`. On a Mac it also shows the words it heard from a test sentence ("Testing the study tools. One, two, three..."). Tell the owner in one line: "Installed and tested. From now on I can study videos on your computer."

**5. The Apify key (so the team pulls posts straight from this computer).** Optional but recommended: without it, every pull goes through the Apify connector in chat, which costs a lot more of the owner's Claude usage on big pulls. The key is a password for their Apify account, so **the owner pastes it into a file themselves. Never ask them to type it in chat, and never put it in a command.** One step per message:
1. "Open apify.com and sign in. Click **Settings** (bottom left), then **API & Integrations**."
2. "Next to **Personal API tokens**, click the copy button on your token (or **Create a new token**, name it Social Media Team, then copy it)."
3. The setup step already made an empty key file, `study-tools/.env` in the home folder (if it's missing, `check-apify` makes it). Tell them where it is: "Open the file `study-tools/.env` in your home folder (on a Mac: Finder, then Go, then Home; on Windows: your user folder). Open it with TextEdit or Notepad, paste your key right after `APIFY_TOKEN=` with no spaces, and save. Tell me when it's saved." On a Mac, TextEdit may hide the file (its name starts with a dot): in Finder press Cmd + Shift + . to show it.
4. Run `python3 STUDY check-apify`. It prints only the Apify username, never the key. "Apify key works. Signed in as: ..." means done. If it says the key wasn't accepted or can't be found, go back to step 2.

Never read the `.env` file back, never show its contents, and never copy the key anywhere else.

Later checks: `python3 STUDY selftest` (about 10 seconds). The script finds the `study-tools` folder by itself, so every stage is always run with plain `python3 STUDY {stage}` (Windows: `python STUDY {stage}`).

## If something goes wrong

Say what happened in one line, then:

| The message says | Do this |
|---|---|
| `python3: command not found` (Mac) or `python is not recognized` (Windows) | Step 2 |
| `Couldn't make the tools folder` | Linux only: install `python3-venv`, then setup again |
| `The install didn't finish` | Check the internet connection, run setup again. Still failing: send the last 10 lines to Claude |
| `Self-test didn't pass` | Run selftest once more. Still failing: the study runs without frames, using Apify's transcripts (as in chat). Say so |
| Cowork can't run commands or download | Use the chat route for the study: Apify transcripts, no frames |
| `I can't find your Apify key yet` | Step 5: the file is missing or the key isn't pasted after `APIFY_TOKEN=` |
| `Apify didn't accept the key` | Step 5, from copying the key again. Check there's no space before or after it |

## Removing it

Delete the `study-tools` folder in the home folder (that also deletes the saved Apify key; the owner can delete the key in Apify too, under API & Integrations). The speech model sits in the computer's cache folder (`.cache/huggingface`); it can be deleted too. The owner's notes in `my-content-team/` stay.
