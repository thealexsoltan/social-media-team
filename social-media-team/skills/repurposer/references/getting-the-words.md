# Getting the words (Step 1)

Every piece is built from the words of the long piece, so get the real words first. Never write from a title, a description, a thumbnail or what the piece is "probably" about. If you can't get the words, say so plainly and ask for them.

Pick the row for what the owner gave you, then use the first route that works on this surface. Tell the owner in one line which route you used ("I read the PDF", "I used YouTube's own captions", "transcribed on your computer").

## Quick table

| The owner gave you | First try | Then | Last |
|---|---|---|---|
| Pasted text, or a text file (.txt, .md) | Read it | A Word file or Google Doc you can't open: ask for a paste or a PDF | |
| A PDF (research paper, ebook, report) | Read it with the Read tool | A scan with no text: say so, ask for a text version | Read the page pictures, every number marked `[check: ...]` |
| A blog post, newsletter or article link | Open the page (web fetch) | Blocked or paywalled: ask for a paste | |
| A YouTube link | YouTube's own captions: the owner pastes "Show transcript", or Apify with captions only (about half a cent, `apify-actors.md`) | Apify transcribes it (about 5 cents a minute) | |
| A podcast link | A transcript on the show's page | The episode's sound file, transcribed on this computer (Claude Code) | The YouTube route, if the episode is on YouTube |
| An Instagram, TikTok or Facebook video link | Owner's own: their captions, or the phone's voice-to-text | Apify transcript (yes and cost first) | |
| The owner's own video or sound file (.mp4, .mov, .m4a, .mp3) | Transcribed on this computer (Claude Code, or Cowork that can run commands) | The recording's own transcript (Zoom, Riverside, phone) | |
| A webinar or call recording | The transcript file that came with it | Transcribed on this computer | |

## Text, files and PDFs

- **Pasted text or a text file:** read it. A file in `my-content-team/` is fine too.
- **A PDF:** open it with the Read tool. A long one (more than 10 pages) is read in page ranges (`pages: "1-10"`, then on). Write down the page number of everything you use.
- **How to tell it's a scan:** the Read tool shows the pages as pictures but gives no words you can search or copy, or the words come out as nonsense. Say it plainly: "This PDF is a scan, so it has no text I can read reliably." Ask for a version with text (the journal's web page, the "HTML" or "full text" link, or a copy from the author's or university's page). If the owner wants to go on anyway, read what the page pictures show, and put `[check: "..."]` on every number and name you took from them.
- **A link to a paper's PDF that won't open or download:** try the article's own web page (journals often show the full text there), then the "free" or "open access" copy the page links to. Still nothing: ask the owner to download the PDF and attach it, or paste the text.
- **Only the abstract (the short summary at the top) is open:** say so. Work from the abstract only, and say in the repurposed file "Read: the abstract only, the full paper is paywalled". Never fill in what the rest of the paper "probably" says.

## Web pages

- If you can open web pages here (web fetch), read the page and say you did. Read the whole page, not the first screen.
- Blocked, paywalled, or you can't open pages here: ask the owner to paste the text. Never write from the title alone.

## YouTube

1. **YouTube's own captions first.** They're free and they're the creator's real words.
   - The owner can get them in a minute: open the video, open the description, press **Show transcript**, copy it and paste it here.
   - Or, with Apify (Claude Code with the owner's Apify key, or the Apify connector): the approved Actor `streamers/youtube-scraper` (from the team's approved list, `apify-actors.md`; use no other), with the video link in `startUrls` and the setting that **only downloads the subtitles already on the video** (check the exact value in the Actor's input before running). One video costs about half a cent ($0.004 a video in `apify-actors.md`; quote that one price, never another). Ask first: "I can pull YouTube's own captions for this video with Apify: about half a cent of your free credit. Or paste the transcript yourself (free). Which?"
2. **The video has no captions:** the same Actor can transcribe it, about 5 cents per minute of video (a 30 minute video is about $1.50). Quote the cost for this video's length and get the owner's yes before running. Set the run's spending limit a little above your quote.
3. **On this computer:** the study tools can transcribe a sound or video **file** for free (see "On this computer" below), but they can't get the sound out of a YouTube link. For the owner's **own** YouTube video: they can download it from YouTube Studio (Content, the three dots next to the video, Download), then give you the file. Never download someone else's YouTube video.

No Apify and no paste: say plainly you can't watch videos, and ask for the transcript with the steps above.

## Podcasts

1. Many shows put a transcript on the episode's web page (look for "Transcript"). Open the page and check.
2. **Claude Code:** the episode's sound file can be transcribed on this computer for free. The link to the file is often on the episode's page ("Download", or the show's RSS feed). It must be a link to the sound file itself (it usually ends in `.mp3` or `.m4a`), not the web page. Then see "On this computer".
3. If the episode is also on YouTube, use the YouTube route.
4. Nothing works: ask the owner to paste the transcript from their podcast app or host.

## Instagram, TikTok and Facebook videos

- **The owner's own:** most of these apps don't give a transcript. Paste the captions if they added them, or play it next to the phone's voice recorder or notes app, which can often turn speech into text.
- **Any public video, with Apify:** only these Actors from the team's approved list (`apify-actors.md`) and their transcript options: Instagram's reel scraper with `includeTranscript` (about 5 cents a minute of sound), TikTok's own captions (free, `clockworks/tiktok-scraper` with `postURLs`; it needs a spending limit of at least $0.50, the real cost is a few cents), Facebook's `captionText`. Yes and cost first.

## On this computer (Claude Code, or Cowork that can run commands)

The Content Researcher's study tools turn speech into text on the owner's computer. Free, and nothing leaves the computer. Don't write your own transcription script: use this one.

- **The script:** `{this skill's folder}/../content-researcher/scripts/study.py`. Claude Code shows this skill's folder when it opens. Put the whole path in double quotes. Below, `STUDY` means that quoted path.
- Run it from the owner's working folder (the one with `my-content-team/` in it). One command at a time, never chained. Windows: `python` instead of `python3`.
- **Is it installed?** `python3 STUDY selftest`. If it says the tools aren't installed: "To transcribe on your computer, the team needs two free tools installed once (a few minutes). Type /team-onboard and say 'set up the study tools'." Or use another route from the table. Don't install anything without telling the owner what it is.
- **One file or one sound link:** `python3 STUDY transcribe-file --file "{full path to the file}" --name {short-name}`, or `--url "{link to the .mp3 or .m4a}"` instead of `--file`. It writes the words with times to `study-tmp/sources/{short-name}.txt`. Read that file. A long recording takes a while (roughly a minute or two per 10 minutes of sound on a recent computer; my guess, older computers are slower). Tell the owner: "Claude may ask you to allow the command, that's normal."
- **If the script says it doesn't know `transcribe-file`** (an older copy of the team), say so in one line and use another route from the table.
- The transcript stays in `study-tmp/`, outside `my-content-team/`. The ideas you take from it go into the repurposed file with their times.

## Whose is it?

Note this once, it changes how you write (`credit-rules.md`):
- **The owner's own** (their video, podcast, live, blog, newsletter, notes).
- **Someone else's** (another creator's video or podcast, another writer's article or newsletter).
- **A research paper** (a study, a report with data).

If it isn't clear, ask in one short line: "Is this yours, or someone else's?" A link to a channel or site that isn't in the profile is someone else's unless the owner says it's theirs.

## Write down what you got

At the top of the repurposed file: what it was, how long, whose, the link, and how you got the words (`repurposed-file.md`). For a paper, also the authors, year, title and where it was published, so every piece can name it.
