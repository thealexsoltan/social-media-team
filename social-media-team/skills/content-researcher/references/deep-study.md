# Deep study: the four hooks, read from the videos themselves

Normally the owner has to type the first spoken line and the first sound of other people's winning videos. Deep study gets them from the videos instead: it downloads the winners, takes still pictures from the first 2 seconds, gets the opening words as text, and labels the four hooks.

## Where it runs

| Surface | Deep study? |
|---|---|
| Claude Code | Yes |
| Cowork (with a folder open) | Yes, if Cowork lets it download files (see "If something fails") |
| claude.ai chat | **No.** Chat can't download a video or run the tools that cut stills from it. Say so plainly and use the screenshot route in `screenshots.md`. One part still works in chat when Apify is on: the spoken words (step 5 below), because the connector returns them as text |

It needs the Apify connector for the video links (`connectors.md`). Without Apify, use the screenshot route.

## The steps

### 1. Pick the videos

- Winners first (outlier score 2.0 or more), best score first. For an account where the whole account is winning (`outlier-score.md`), take its top views among the posts used for the normal.
- **At most 10 videos per run** unless the owner asks for more. 3 per account is plenty.
- Instagram and TikTok only. Other platforms: screenshot route.

### 2. Ask first (same as every Apify pull)

List the videos (account, views, score), the rough cost and the time, then wait for a yes. Nothing is downloaded or paid for before that. Example:

> I can read the hooks from these 3 TikTok videos myself: @handle 108,800 (7.1), @handle 83,600 (5.4), @handle 65,500 (4.3). That costs about 2 cents of your free Apify credit and takes about 5 minutes. Claude may ask you to allow a few commands while I work, that's normal. Go ahead?

Rough costs (Apify free plan prices, checked 2026-11-04, they can change; only Actors from `apify-actors.md`):
- TikTok: about half a cent per video, captions free.
- Instagram: about 5 cents a minute of sound for the spoken words (the reel scraper's transcript add-on). The video itself comes free with the normal pull, but only for 1 to 3 days. If the pull is older, re-pull the reels by link first (about a quarter of a cent each).
- Time: about 1 to 2 minutes per video.

If the Apify tool lets you set a spending limit, set it a little above the estimate (`clockworks/tiktok-scraper` needs at least $0.50, see `connectors.md`).

### 3. Get the video links

From the Apify pull (field names in `connectors.md`, "Videos and spoken words"):
- **Instagram:** `videoUrl` from the reel pull. Older than a day or two? Run `apify/instagram-reel-scraper` again with the reel links in `username` (add `includeTranscript: true` to get the words in the same run).
- **TikTok:** run `clockworks/tiktok-scraper` with `postURLs` set to the winners' `webVideoUrl`, `shouldDownloadVideos: true` and `downloadSubtitlesOptions: DOWNLOAD_SUBTITLES`. The video link is in `mediaUrls`, the caption file in `videoMeta.subtitleLinks`.

### 4. Download, then cut stills and sound

Work in a scratch folder called `deep-study-tmp/` in the working folder, **never** inside `my-content-team/`. Run one simple command at a time (no chains), so each permission prompt is easy to read. Name files by account and views, like `handle-108800`.

```
mkdir -p deep-study-tmp
curl -sL -o deep-study-tmp/handle-108800.mp4 "VIDEO LINK"
ffmpeg -v error -ss 0 -i deep-study-tmp/handle-108800.mp4 -frames:v 1 -vf scale=540:-2 deep-study-tmp/handle-108800-0s.jpg
ffmpeg -v error -ss 1 -i deep-study-tmp/handle-108800.mp4 -frames:v 1 -vf scale=540:-2 deep-study-tmp/handle-108800-1s.jpg
ffmpeg -v error -ss 2 -i deep-study-tmp/handle-108800.mp4 -frames:v 1 -vf scale=540:-2 deep-study-tmp/handle-108800-2s.jpg
ffmpeg -v error -i deep-study-tmp/handle-108800.mp4 -t 5 -vn -ac 1 -ar 16000 deep-study-tmp/handle-108800-5s.wav
```

No `ffmpeg`? Check with `ffmpeg -version`. To add it: `python3 -m pip install imageio-ffmpeg`, then `python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` prints the path to use in place of `ffmpeg`. On a Mac with Homebrew, `brew install ffmpeg` works too.

The sound file is only needed for step 5, route C.

### 5. Get the opening words as text

Pick the first route that works. None needs an OpenAI or Google key.

| Route | Platform | How | Cost |
|---|---|---|---|
| **A. TikTok's own captions** | TikTok | The caption file from step 3 (`subtitleLinks`, `downloadLink`). Read it with the connector's key-value store tool, or download it with `curl` | Free |
| **B. Apify transcript** | Instagram | The reel scraper's `includeTranscript: true` on the reel links (`apify-actors.md`). Only if that sends nothing: `invideoiq/video-transcriber` (`video_urls`: the links), the last resort | About 5 cents a minute of sound (last resort: 3.5 cents a video) |
| **C. Free tool on the computer** | Either | Claude Code only: `python3 -m pip install openai-whisper`, then `whisper deep-study-tmp/handle-108800-5s.wav --model base --language en --output_format txt --output_dir deep-study-tmp`. Runs on the computer, no account. The first run downloads a model of about 140 MB | Free |
| **D. Ask the owner** | Either | "Play it with the sound on and type the first sentence you hear" | Free |

Keep only the first sentence or so (the first 2 to 5 seconds). Machine-made words can mishear a word ("papers" for "peepers"). Check them against the words on screen, and mark the line `(machine heard)`.

### 6. Read the stills

Open the three stills (Read the image files) and write only what you see:
- **First frame:** the 0 second still, in one line.
- **Text hook:** words on screen in the 0, 1 and 2 second stills, word for word. A text box that stays on screen is the text hook. Big single words that pop up one at a time and match the speech are spoken captions, not a text hook: write them as "word-by-word captions of the speech".
- **Format:** what most of the three stills look like, using only the words in `formats.md`. Three stills are a small window, so mark it "(from the first 2 seconds)".

### 7. First sound

Claude can't listen to sound. Use what the data says:
- Words start in the first half second (by the transcript or caption times): first sound is `voice, talking from the start`.
- The pull's music field: Instagram `musicInfo.song_name`, TikTok `musicMeta.musicName`. "Original audio" or "original sound" means their own sound. A song name means a track, write its name.
- A noise like clippers or water can't be heard by us: write `not seen` unless the owner tells you.

### 8. Label and mark the source of everything

Fill the winner checklist in `studying-winners.md` as usual, with the hook type and format from `formats.md`. After each line, say where it came from:

| Source tag | Means |
|---|---|
| `video still` | Read from a still taken from the video at 0, 1 or 2 seconds |
| `TikTok captions` | TikTok's own captions, through Apify |
| `Apify transcript` | Route B |
| `machine heard on this computer` | Route C |
| `music info` | The pull's music field |
| `owner typed it` | Route D |

In `research-notes.md`, the winner's "Seen from" line gets `Deep study` plus the tags used. Anything no route gave you stays `not seen`. Never fill a gap from what videos like this "usually" do.

### 9. Clean up

Delete `deep-study-tmp/` when the notes are written (it holds other people's videos). Only the notes stay, in `my-content-team/`. Say in one line that the videos were deleted.

## If something fails

Say what happened in one line, then fall back for that step only. Never stop the whole study.

| Problem | Fallback |
|---|---|
| Chat, no file tools | Screenshot route (`screenshots.md`). Spoken words through Apify still work (route A or B) |
| Download blocked or fails (Cowork may only be allowed to reach code stores) | "Cowork couldn't download the video, its internet setting may be limited. You can allow more in Claude's Settings, under Capabilities, or send me a screenshot of the first second." Spoken words through Apify still work |
| Video link expired | Re-pull the post by its link (step 3) |
| `ffmpeg` missing and can't be added | Ask for a screenshot of the first second of each video |
| No captions and no transcript | Route C, then route D |
| Private or deleted video | Skip it, say which one |
| Apify credit used up | The message in `connectors.md`, then screenshots |

Show the same source tag next to every hook in the reply as well as in `research-notes.md`.
