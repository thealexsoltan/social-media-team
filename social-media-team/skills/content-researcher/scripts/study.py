#!/usr/bin/env python3
"""
Study accounts: the Content Researcher's reel study tool.

Run it from the owner's working folder (the folder that holds my-content-team/).
One stage at a time:

  python3 study.py plan          which Claude plan this is (reads 2 fields only)
  python3 study.py setup         install the tools once (faster-whisper + imageio-ffmpeg)
  python3 study.py selftest      10 second check that the tools work
  python3 study.py check-apify   check the Apify key in study-tools/.env works (prints the username only)
  python3 study.py pull --instagram a,b --tiktok c --posts 30 --budget 0.50
                                 run the Apify scrapers from here, save to study-tmp/pulls/
  python3 study.py stats         Apify pulls in study-tmp/pulls/ -> stats.md + dashboard.html
  python3 study.py pick --total 6     choose the reels to study (or --codes A,B,C)
  python3 study.py download      picked videos -> study-tmp/videos/
  python3 study.py transcribe    timed transcripts, on this computer, free
  python3 study.py transcribe-file --file talk.mp4 --name my-talk
                                 one long piece (a file, or --url to an .mp3), for the Repurposer
  python3 study.py frames        hook frames, 1 per second contact sheets, cut detection
  python3 study.py stubs         one breakdown stub per picked reel, facts filled in
  python3 study.py cleanup       delete the downloaded videos (add --all for all of study-tmp)

Where things go:
  study-tmp/pulls/*.json                  the Apify pulls (saved by Claude)
  study-tmp/picks.json, videos/, thumbs/  temporary, never inside my-content-team/
  study-tmp/sources/<name>.txt, .json      one long piece's words (transcribe-file), never inside my-content-team/
  my-content-team/study/<handle>/         stats.md, transcripts/, frames/, breakdowns/
  my-content-team/study/dashboard.html    every account in one page

Needs Python 3.9 or newer. stats, pick, download, cleanup and plan use only Python itself.
transcribe needs faster-whisper; frames needs ffmpeg (a system ffmpeg, or imageio-ffmpeg).
Only pull and check-apify use a key: the owner's Apify key, read from study-tools/.env and never printed.
"""
import argparse
import base64
import datetime as dt
import html
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
DEFAULT_MODEL = "base.en"
WINNER = 2.0
MAX_NORMAL_POSTS = 30
MIN_AGE_DAYS = 3
VENV_DIR = Path(os.environ.get("STUDY_TOOLS_DIR") or (Path.home() / "study-tools"))
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Whisper makes up short stock lines on music. These never count as speech.
HALLU = re.compile(
    r"^(thank you\.?|thanks for watching!?|you|bye\.?|\.+|\u266a+|music|\[music\]|okay\.?|oh\.?|"
    r"subscribe.*|please subscribe.*|i'll see you (in the )?next (one|time|video)\.?)$",
    re.I,
)

try:  # Windows consoles choke on emoji in captions
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:
    pass


def rhu(x, nd=0):
    """Round half up, one rule everywhere (Python's round() rounds 0.5 to even)."""
    if x is None:
        return None
    q = Decimal(str(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return int(q) if nd == 0 else float(q)


def say(msg=""):
    print(msg, flush=True)


def fail(msg):
    say(msg)
    sys.exit(1)


# ---------------------------------------------------------------- paths


class Paths:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.team = self.root / "my-content-team"
        self.study = self.team / "study"
        self.tmp = self.root / "study-tmp"
        self.pulls = self.tmp / "pulls"
        self.videos = self.tmp / "videos"
        self.thumbs = self.tmp / "thumbs"
        self.sources = self.tmp / "sources"  # transcribe-file: one long piece for the Repurposer
        self.picks = self.tmp / "picks.json"
        self.state = self.tmp / "study-state.json"  # the date and normals stats used: every later stage reads them

    def account(self, handle):
        return self.study / handle


def safe_name(s):
    s = re.sub(r"[^A-Za-z0-9._]+", "", str(s or "").lstrip("@").strip().lower())
    return s or "unknown"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- tools on this computer


def venv_python():
    for p in (VENV_DIR / "bin" / "python", VENV_DIR / "Scripts" / "python.exe"):
        if p.exists():
            return p
    return None


def rerun_in_venv(what):
    """The stage needs a package this Python doesn't have. Use the study-tools copy if it exists."""
    vp = venv_python()
    if vp and Path(sys.prefix).resolve() != VENV_DIR.resolve() and not os.environ.get("STUDY_IN_VENV"):
        env = dict(os.environ, STUDY_IN_VENV="1", KMP_DUPLICATE_LIB_OK="TRUE")
        sys.exit(subprocess.call([str(vp), str(Path(__file__).resolve())] + sys.argv[1:], env=env))
    fail(f"{what} isn't installed yet. Run this once, then try again:\n"
         f"  python3 \"{Path(__file__).resolve()}\" setup")


_FFMPEG = {}


def _ffmpeg_candidates():
    cands = []
    try:  # the bundled copy first: it can print text on pictures (some system copies can't)
        import imageio_ffmpeg  # noqa: F401
        cands.append(imageio_ffmpeg.get_ffmpeg_exe())
    except Exception:
        pass
    # the copy that setup installed into the study-tools folder
    cands += [str(p) for p in sorted(VENV_DIR.glob("**/imageio_ffmpeg/binaries/ffmpeg*")) if not p.name.endswith(".md")]
    if shutil.which("ffmpeg"):
        cands.append(shutil.which("ffmpeg"))
    return cands


def _has_drawtext(c):
    try:
        out = subprocess.run([c, "-hide_banner", "-filters"], capture_output=True, text=True, errors="replace", timeout=30).stdout
        return bool(re.search(r"\sdrawtext\s", out))
    except Exception:
        return False


def ffmpeg_exe(required=True, drawtext=False):
    """A working ffmpeg. With drawtext=True, only one that can print the time on a picture (None if there's none)."""
    if drawtext in _FFMPEG:
        return _FFMPEG[drawtext]
    found = None
    for c in _ffmpeg_candidates():
        try:
            if subprocess.run([c, "-hide_banner", "-version"], capture_output=True, timeout=30).returncode != 0:
                continue
        except Exception:
            continue
        if not drawtext or _has_drawtext(c):
            found = c
            break
    _FFMPEG[drawtext] = found
    if found or drawtext:
        return found
    if required:
        rerun_in_venv("The video tool (ffmpeg)")
    return None


def run(cmd, timeout=600):
    return subprocess.run([str(c) for c in cmd], capture_output=True, text=True, errors="replace", timeout=timeout)


def probe(video):
    """Duration in seconds and whether there's a sound track, read from ffmpeg's own report."""
    err = run([ffmpeg_exe(), "-hide_banner", "-i", video]).stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", err)
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0
    return dur, bool(re.search(r"Stream #.*Audio:", err))


def font_file():
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc",
              "/Library/Fonts/Arial.ttf", "C:/Windows/Fonts/arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(p).exists():
            return p
    return None


def label_filter(size, font=True):
    """A drawtext filter that prints each tile's time on it."""
    f = font_file() if font else None
    font = "fontfile='{}':".format(f.replace("\\", "/").replace(":", "\\:")) if f else ""
    return (f"drawtext={font}text='%{{pts\\:hms}}':x=6:y=6:fontsize={size}:fontcolor=white:"
            "box=1:boxcolor=black@0.65:boxborderw=4,")


# ---------------------------------------------------------------- reading the Apify pulls


def num(v):
    if v is None or isinstance(v, bool):
        return None
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return None if v < 0 else v


def parse_date(v):
    if v in (None, ""):
        return None
    try:
        if isinstance(v, (int, float)) or str(v).isdigit():
            return dt.datetime.fromtimestamp(int(v), tz=dt.timezone.utc)
        return dt.datetime.fromisoformat(str(v).replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except Exception:
        return None


def load_items(paths):
    files = sorted(paths.pulls.glob("*.json"), key=lambda p: p.stat().st_mtime) if paths.pulls.exists() else []
    items = []
    for f in files:
        try:
            data = read_json(f)
        except Exception as e:
            say(f"  skipped {f.name}: not a readable JSON file ({e})")
            continue
        if isinstance(data, dict):
            data = data.get("items") or data.get("data") or [data]
        for it in data if isinstance(data, list) else []:
            if isinstance(it, dict):
                items.append((f.stem, it))
    return files, items


def normalize(src, it):
    """One post in one shape, whatever Actor it came from. Returns ('post', dict) or ('followers', (handle, n))."""
    if it.get("error") or it.get("errorDescription"):
        return None
    if it.get("shortCode") or (it.get("type") in ("Video", "Image", "Sidecar") and it.get("url")):  # Instagram post
        code = it.get("shortCode") or re.sub(r".*/(p|reel)/([^/?]+).*", r"\2", it.get("url", ""))
        handle = safe_name(it.get("ownerUsername") or src)
        kind = {"Video": "video", "Image": "photo", "Sidecar": "carousel"}.get(it.get("type"), "video" if it.get("videoUrl") else "photo")
        music = it.get("musicInfo") or {}
        m = re.match(r"https?://(www\.)?instagram\.com/([A-Za-z0-9._]+)/?$", str(it.get("inputUrl") or ""))
        post = {
            "platform": "Instagram", "handle": handle, "input_handle": safe_name(m.group(2)) if m else None, "code": code,
            "url": it.get("url") or f"https://www.instagram.com/p/{code}/",
            "kind": kind, "date": parse_date(it.get("timestamp")),
            "plays": num(it.get("videoPlayCount")), "views_alt": num(it.get("videoViewCount")),
            "likes": num(it.get("likesCount")), "comments": num(it.get("commentsCount")),
            # shares come only from the reel scraper's paid shares add-on; saves are never in the public data
            "shares": next((num(it.get(k)) for k in ("sharesCount", "shareCount", "reshareCount") if num(it.get(k)) is not None), None),
            "saves": None, "length": num(it.get("videoDuration")),
            "caption": it.get("caption") or "", "pinned": bool(it.get("isPinned")),
            "video_url": it.get("videoUrl"), "audio_url": it.get("audioUrl"),
            "thumb_url": it.get("displayUrl"),
            "music": " by ".join(x for x in (music.get("song_name"), music.get("artist_name")) if x) or None,
        }
        meta = it.get("metaData") or {}
        fol = num(meta.get("followersCount")) or num(it.get("ownerFollowersCount"))
        return "post", post, (handle, fol) if fol else None
    if it.get("followersCount") is not None and (it.get("username") or it.get("userName")):  # Instagram profile
        return "followers", None, (safe_name(it.get("username") or it.get("userName")), num(it.get("followersCount")))
    if it.get("webVideoUrl") or it.get("playCount") is not None or it.get("authorMeta"):  # TikTok video
        a = it.get("authorMeta") or {}
        vm = it.get("videoMeta") or {}
        mm = it.get("musicMeta") or {}
        handle = safe_name(a.get("name") or a.get("uniqueId") or src)
        media = it.get("mediaUrls") or []
        post = {
            "platform": "TikTok", "handle": handle, "code": str(it.get("id") or ""),
            "url": it.get("webVideoUrl") or "", "kind": "slideshow" if it.get("isSlideshow") else "video",
            "date": parse_date(it.get("createTimeISO") or it.get("createTime")),
            "plays": num(it.get("playCount")), "views_alt": None,
            "likes": num(it.get("diggCount")), "comments": num(it.get("commentCount")),
            "shares": num(it.get("shareCount")), "saves": num(it.get("collectCount")),
            "length": num(vm.get("duration")), "caption": it.get("text") or "",
            "pinned": bool(it.get("isPinned")), "video_url": media[0] if media else None,
            "audio_url": None, "thumb_url": vm.get("coverUrl") or vm.get("originalCoverUrl"),
            "music": mm.get("musicName"),
        }
        fol = num(a.get("fans"))
        return "post", post, (handle, fol) if fol else None
    return None


def load_accounts(paths, extra_followers=()):
    files, items = load_items(paths)
    posts, followers, by_file = {}, {}, {}
    for src, it in items:
        r = normalize(src, it)
        if not r:
            continue
        kind, post, fol = r
        if fol and fol[1]:
            followers[fol[0]] = fol[1]
        if kind == "post" and post["code"]:
            by_file.setdefault(src, []).append(post)
    for src, fposts in by_file.items():
        # A collab post can carry the other creator's name. Keep it with the account that was pulled.
        counts = {}
        for p in fposts:
            counts[p["handle"]] = counts.get(p["handle"], 0) + 1
        known = {h for h, n in counts.items() if n >= 3} | {p["input_handle"] for p in fposts if p.get("input_handle")}
        main = max(counts, key=counts.get)
        for p in fposts:
            if p.get("input_handle"):
                p["handle"] = p["input_handle"]
            elif p["handle"] not in known:
                p["handle"] = main
    for post in (p for fposts in by_file.values() for p in fposts):  # files in time order: newer numbers win
        key = (post["platform"], post["code"])
        old = posts.get(key, {})
        posts[key] = {**old, **{k: v for k, v in post.items() if v not in (None, "")}}
        for k, v in post.items():
            posts[key].setdefault(k, v)
    for pair in extra_followers:
        h, _, n = pair.partition("=")
        if num(n):
            followers[safe_name(h)] = num(n)
    accounts = {}
    for p in posts.values():
        accounts.setdefault(p["handle"], []).append(p)
    return files, {h: account_stats(h, ps, followers.get(h)) for h, ps in sorted(accounts.items())}


# ---------------------------------------------------------------- the numbers


def today_utc(args):
    if getattr(args, "today", None):
        return dt.datetime.fromisoformat(args.today).replace(tzinfo=dt.timezone.utc)
    return dt.datetime.now(dt.timezone.utc)


TODAY = None


def account_stats(handle, posts, followers):
    posts = sorted(posts, key=lambda p: p["date"] or dt.datetime.min.replace(tzinfo=dt.timezone.utc), reverse=True)
    platform = posts[0]["platform"]
    field = "videoPlayCount" if platform == "Instagram" else "playCount"
    if platform == "Instagram" and not any(p["plays"] for p in posts if p["kind"] == "video"):
        field = "videoViewCount"
    for p in posts:
        p["views"] = p["plays"] if field in ("videoPlayCount", "playCount") else p["views_alt"]
        p["age_days"] = (TODAY - p["date"]).total_seconds() / 86400 if p["date"] else None
        p["too_new"] = p["age_days"] is not None and p["age_days"] < MIN_AGE_DAYS
    viewed = [p for p in posts if p["views"] is not None and p["kind"] in ("video", "slideshow")]
    used = [p for p in viewed if not p["pinned"] and not p["too_new"]][:MAX_NORMAL_POSTS]
    normal = rhu(statistics.median([p["views"] for p in used])) if used else None
    for p in posts:
        p["score_raw"] = p["views"] / normal if normal and p["views"] is not None else None
        p["score"] = rhu(p["score_raw"], 1) if p["score_raw"] is not None else None
        p["used"] = p in used
    scored = [p for p in viewed if not p["pinned"] and not p["too_new"] and p["score"] is not None]

    def per_k(key):
        vals = [p[key] / p["views"] * 1000 for p in used if p.get(key) is not None and p["views"]]
        return rhu(statistics.median(vals), 1) if vals else None

    dates = [p["date"] for p in posts if p["date"]]
    # posts per week over the last 8 weeks only (a long pull can have gaps further back)
    window = min(56.0, (TODAY - min(dates)).total_seconds() / 86400) if dates else 0
    recent = [d for d in dates if (TODAY - d).total_seconds() / 86400 <= window]
    per_week = rhu(len(recent) / (window / 7), 1) if window >= 14 else None
    by_day = {}
    for p in scored:
        if p["date"]:
            by_day.setdefault(p["date"].weekday(), []).append(p["score"])
    lengths = [p["length"] for p in used if p["length"]]
    return {
        "handle": handle, "platform": platform, "posts": posts, "field": field,
        "followers": followers, "used": used, "normal": normal, "scored": scored,
        "n_video": sum(p["kind"] in ("video", "slideshow") for p in posts),
        "n_other": sum(p["kind"] in ("photo", "carousel") for p in posts),
        "pinned": [p for p in posts if p["pinned"]],
        "too_new": [p for p in posts if p["too_new"]],
        "first": min(dates) if dates else None, "last": max(dates) if dates else None,
        "per_week": per_week, "per_week_weeks": rhu(window / 7) if window >= 14 else None,
        "reach": rhu(normal / followers, 2) if normal and followers else None,
        "likes_k": per_k("likes"), "comments_k": per_k("comments"),
        "shares_k": per_k("shares"), "saves_k": per_k("saves"),
        "has_shares": any(p.get("shares") is not None for p in posts),
        "length": rhu(statistics.median(lengths)) if lengths else None,
        "winners_used": sum(1 for p in used if p["score"] is not None and p["score"] >= WINNER),
        "winners_all": sum(1 for p in scored if p["score"] >= WINNER),
        "days": {d: (len(v), rhu(statistics.median(v), 1)) for d, v in sorted(by_day.items())},
        "top": sorted(scored, key=lambda p: p["score_raw"], reverse=True)[:10],
    }


def fmt(n, dec=0, none="not in the pull"):
    if n is None:
        return none
    return f"{n:,.{dec}f}"


def plural(n, word, many=None):
    return f"{n} {word if n == 1 else (many or word + 's')}"


def short(text, n=70):
    t = re.sub(r"\s+", " ", text or "").strip()
    return (t[: n - 3].rstrip() + "...") if len(t) > n else t


def cell(text):
    return (text or "").replace("|", "/").replace("\n", " ")


def score_txt(p):
    return f"{p['score']:.1f}" if p.get("score") is not None else "not scored"


def stats_md(a):
    ig = a["platform"] == "Instagram"
    nopub = "not in the public data (Instagram)"
    noshare = "not in the public data (Instagram shares weren't pulled: a paid Apify add-on)"
    show_shares = (not ig) or a["has_shares"]
    fol = f"{fmt(a['followers'])} (Apify)" if a["followers"] else "not in the pull (ask the owner, or add a profile pull)"
    reach = (f"{fmt(a['normal'])} ÷ {fmt(a['followers'])} = {a['reach']:.2f}" if a["reach"] is not None
             else "not checked (no follower count)")
    small = " (small sample, under 9 posts)" if len(a["used"]) < 9 else ""
    left_out = []
    if a["pinned"]:
        left_out.append(f"{len(a['pinned'])} pinned")
    if a["too_new"]:
        left_out.append(f"{len(a['too_new'])} under {MIN_AGE_DAYS} days old")
    L = [f"# @{a['handle']}: account numbers",
         f"Made: {TODAY:%Y-%m-%d}, from an Apify pull ({a['platform']}). Every number here is marked Apify.",
         "Score (outlier score) = a post's views ÷ the account's normal. 2.0 or more is a winner.", "",
         "## In one look", "", "| | |", "|---|---|",
         f"| Followers | {fol} |",
         f"| Posts pulled | {len(a['posts'])} ({plural(a['n_video'], 'video')}, {a['n_other']} {'photo or carousel' if a['n_other'] == 1 else 'photos or carousels'}) |",
         f"| Dates | {a['first']:%Y-%m-%d} to {a['last']:%Y-%m-%d} |" if a["first"] else "| Dates | not in the pull |",
         (f"| Posts per week | {a['per_week']} (last {a['per_week_weeks']} weeks only, so older gaps don't count) |"
          if a["per_week"] is not None else "| Posts per week | not enough recent posts to tell (under 2 weeks) |"),
         f"| Normal (middle views) | {fmt(a['normal'])}, from the newest {len(a['used'])} videos{small}"
         + (f"; left out: {', '.join(left_out)}" if left_out else "") + " |",
         f"| Views number used | `{a['field']}` |",
         f"| Reach (normal ÷ followers) | {reach} |",
         f"| Likes per 1,000 views | {fmt(a['likes_k'], 1)} (middle post) |",
         f"| Comments per 1,000 views | {fmt(a['comments_k'], 1)} (middle post) |",
         f"| Shares per 1,000 views | {fmt(a['shares_k'], 1) + ' (middle post)' if show_shares else noshare} |",
         f"| Saves per 1,000 views | {nopub if ig else fmt(a['saves_k'], 1) + ' (middle post)'} |",
         f"| Middle length | {a['length']} seconds |" if a["length"] else "| Middle length | not in the pull |",
         f"| Winners (2.0 or more) | {a['winners_used']} of {len(a['used'])} in the posts used for the normal; "
         f"{a['winners_all']} of {len(a['scored'])} in the whole pull |", ""]
    if a["n_other"] and ig:
        L += [f"Photos and carousels have no view count in the public data, so they aren't scored.", ""]
    L += ["## Best posting days", "",
          "Days are in UTC time, so a late night post can land on the next day. Under 3 videos on a day is too few to tell.", "",
          "| Day | Videos | Middle score |", "|---|---|---|"]
    L += [f"| {DAYS[d]} | {n} | {m:.1f}{' (too few)' if n < 3 else ''} |" for d, (n, m) in a["days"].items()] or ["| not enough dated posts | | |"]
    L += ["", "## Top 10 by score", "",
          "| # | Date | Views | Score | Sum | Likes | Comments | Length | Caption starts | Link |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for i, p in enumerate(a["top"], 1):
        L.append(f"| {i} | {p['date']:%Y-%m-%d} | {fmt(p['views'])} | {score_txt(p)} | {fmt(p['views'])} ÷ {fmt(a['normal'])} | "
                 f"{fmt(p['likes'], none='not visible')} | {fmt(p['comments'], none='not visible')} | {fmt(p['length'], 1, none='?')}s | {cell(short(p['caption'], 60))} | {p['url']} |")
    if a["pinned"]:
        L += ["", "## All-time hits (pinned, left out of the normal)", "", "| Date | Views | Link |", "|---|---|---|"]
        L += [f"| {p['date']:%Y-%m-%d} | {fmt(p['views'])} | {p['url']} |" for p in a["pinned"] if p["date"]]
    L += ["", "## Every post", "",
          "| Date | Type | Views | Score | Likes | Comments | " + ("Shares | " if show_shares else "") + ("" if ig else "Saves | ")
          + "Length | Note | Code |",
          "|---|---|---|---|---|---|" + ("---|" if show_shares else "") + ("" if ig else "---|") + "---|---|---|"]
    for p in a["posts"]:
        note = "pinned" if p["pinned"] else f"under {MIN_AGE_DAYS} days old" if p["too_new"] else ("winner" if (p["score"] or 0) >= WINNER else "")
        extra = (f"{fmt(p['shares'], none='not visible')} | " if show_shares else "") + ("" if ig else f"{fmt(p['saves'], none='not visible')} | ")
        L.append(f"| {p['date']:%Y-%m-%d} | {p['kind']} | {fmt(p['views']) if p['views'] is not None else 'no views shown'} | "
                 f"{score_txt(p) if p['score'] is not None else ''} | {fmt(p['likes'], none='not visible')} | {fmt(p['comments'], none='not visible')} | {extra}"
                 f"{fmt(p['length'], 1) + 's' if p['length'] else ''} | {note} | {p['code']} |" if p["date"] else
                 f"| no date | {p['kind']} | {fmt(p['views'])} | {score_txt(p)} | | | {extra} | | {p['code']} |")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- dashboard


def fetch(url, dest, timeout=60):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def thumb_data(paths, p):
    if not p.get("thumb_url") or not ffmpeg_exe(required=False):
        return None
    d = paths.thumbs / p["handle"]
    small = d / f"{p['code']}.jpg"
    if not small.exists():
        try:
            d.mkdir(parents=True, exist_ok=True)
            raw = fetch(p["thumb_url"], d / f"{p['code']}.raw", timeout=10)
            run([ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-i", raw, "-vf", "scale=96:-2", "-q:v", "5", small], timeout=30)
            if raw.exists():
                raw.unlink()
            if not small.exists():
                return None
        except Exception:
            return None
    try:
        b = small.read_bytes()
        return "data:image/jpeg;base64," + base64.b64encode(b).decode() if len(b) < 200_000 else None
    except Exception:
        return None


DASH = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Account study</title>
<style>
:root{--bg:#faf9f5;--card:#fff;--ink:#1f1e1b;--muted:#6b6862;--line:#e6e3da;--win:#1f7a4d;--winbg:#e5f3ea;--accent:#c4643f}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--card:#252421;--ink:#eeebe3;--muted:#a5a199;--line:#3a3833;--win:#6fd09c;--winbg:#1f3529;--accent:#e08a66}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:1200px;margin:0 auto;padding:20px 16px 60px}h1{font-size:24px;margin:0 0 4px}h2{font-size:18px;margin:28px 0 10px}
.sub{color:var(--muted);margin:0 0 18px}.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}.card h3{margin:0 0 8px;font-size:16px}
.kv{display:grid;grid-template-columns:1fr auto;gap:2px 10px;font-size:13px}.kv span:nth-child(odd){color:var(--muted)}
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0}select,input{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}table{border-collapse:collapse;width:100%;font-size:13px}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle;white-space:nowrap}th{cursor:pointer;user-select:none;position:sticky;top:0;background:var(--card)}
td.cap{white-space:normal;min-width:220px;max-width:380px}td.n{text-align:right;font-variant-numeric:tabular-nums}
tr.win td.sc{color:var(--win);font-weight:700;background:var(--winbg)}img{width:44px;height:auto;border-radius:6px;display:block}
a{color:var(--accent)}.muted{color:var(--muted)}
</style></head><body><main>
<h1>Account study</h1><p class="sub" id="sub"></p>
<div class="cards" id="cards"></div>
<h2>Every post</h2>
<div class="bar"><label>Account <select id="acc"><option value="">All</option></select></label>
<label><input type="checkbox" id="wins"> Winners only</label><span class="muted">Click a column to sort.</span></div>
<div class="wrap"><table><thead><tr id="head"></tr></thead><tbody id="rows"></tbody></table></div>
<p class="muted">Score = views ÷ that account's normal (its middle views). 2.0 or more is a winner. Pinned posts and posts under 3 days old are left out of the normal. All numbers came from Apify.</p>
</main><script>
const D=__DATA__;
const $=s=>document.querySelector(s);const f=n=>n==null?"":Math.round(n).toLocaleString();
const np=p=>p.platform==="Instagram"?"<span class=muted>not public</span>":"";
const esc=t=>String(t??"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
$("#sub").textContent=D.made+" \\u00b7 "+D.accounts.length+" accounts \\u00b7 "+D.posts.length+" posts";
for(const a of D.accounts){const c=document.createElement("div");c.className="card";
const kv=[["Platform",a.platform],["Followers",a.followers?f(a.followers):"not in the pull"],["Normal views",a.normal?f(a.normal):"not enough posts"],
["Reach",a.reach!=null?a.reach.toFixed(2):"not checked"],["Winners",a.winners],["Posts per week",a.per_week??""],["Likes per 1,000 views",a.likes_k??""],
["Comments per 1,000 views",a.comments_k??""],["Shares per 1,000 views",a.shares_k??"not in the public data"],["Middle length",a.length?a.length+"s":""]];
c.innerHTML="<h3>@"+a.handle+"</h3><div class=kv>"+kv.map(([k,v])=>"<span>"+k+"</span><span>"+v+"</span>").join("")+"</div>";
$("#cards").appendChild(c);const o=document.createElement("option");o.value=o.textContent=a.handle;$("#acc").appendChild(o);}
const cols=[["","thumb"],["Account","handle"],["Date","date"],["Type","kind"],["Views","views",1],["Score","score",1],["Likes","likes",1],["Comments","comments",1],["Shares","shares",1],["Saves","saves",1],["Length","length",1],["Caption","caption"]];
let key="score",dir=-1;
$("#head").innerHTML=cols.map(c=>"<th data-k='"+c[1]+"'>"+c[0]+"</th>").join("");
document.querySelectorAll("th").forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(k==="thumb")return;dir=key===k?-dir:-1;key=k;draw();});
function draw(){const acc=$("#acc").value,w=$("#wins").checked;
let r=D.posts.filter(p=>(!acc||p.handle===acc)&&(!w||(p.score||0)>=2));
const sk=key==="score"?"score_sort":key;r.sort((a,b)=>{const x=a[sk],y=b[sk];if(x==null)return 1;if(y==null)return -1;return (x>y?1:x<y?-1:0)*dir;});
$("#rows").innerHTML=r.map(p=>"<tr class='"+((p.score||0)>=2?"win":"")+"'><td>"+(p.thumb?"<img alt='' src='"+p.thumb+"'>":"")+"</td><td>@"+p.handle+"</td><td>"+p.date+"</td><td>"+p.kind+(p.note?" <span class=muted>("+p.note+")</span>":"")+
"</td><td class=n>"+f(p.views)+"</td><td class='n sc'>"+(p.score!=null?p.score.toFixed(1):"")+"</td><td class=n>"+f(p.likes)+"</td><td class=n>"+f(p.comments)+"</td><td class=n>"+(p.shares==null?np(p):f(p.shares))+"</td><td class=n>"+(p.saves==null?np(p):f(p.saves))+
"</td><td class=n>"+(p.length?Math.round(p.length)+"s":"")+"</td><td class=cap><a href='"+esc(p.url)+"' target=_blank rel=noopener>open</a> "+esc(p.caption)+"</td></tr>").join("");}
$("#acc").onchange=draw;$("#wins").onchange=draw;draw();
</script></body></html>
"""


def write_dashboard(paths, accounts, thumbs=True):
    allp = [p for a in accounts.values() for p in a["posts"]]
    td = {}
    if thumbs:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for p, t in zip(allp, pool.map(lambda p: thumb_data(paths, p), allp)):
                td[(p["platform"], p["code"])] = t
    data = {
        "made": f"Made {TODAY:%Y-%m-%d}",
        "accounts": [{"handle": a["handle"], "platform": a["platform"], "followers": a["followers"], "normal": a["normal"],
                      "reach": a["reach"], "winners": f"{a['winners_used']} of {len(a['used'])}", "per_week": a["per_week"],
                      "likes_k": a["likes_k"], "comments_k": a["comments_k"],
                      "shares_k": a["shares_k"] if (a["platform"] != "Instagram" or a["has_shares"]) else None, "length": a["length"]}
                     for a in accounts.values()],
        "posts": [{"handle": p["handle"], "platform": p["platform"], "date": f"{p['date']:%Y-%m-%d}" if p["date"] else "", "kind": p["kind"],
                   "views": p["views"], "score": p["score"] if not (p["pinned"] or p["too_new"]) else None,
                   "score_sort": p["score_raw"] if not (p["pinned"] or p["too_new"]) else None,
                   "likes": p["likes"], "comments": p["comments"], "shares": p["shares"], "saves": p["saves"],
                   "length": p["length"], "caption": short(p["caption"], 140), "url": p["url"],
                   "note": "pinned" if p["pinned"] else "too new" if p["too_new"] else "",
                   "thumb": td.get((p["platform"], p["code"]))} for p in allp],
    }
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    write(paths.study / "dashboard.html", DASH.replace("__DATA__", blob))
    return sum(1 for v in td.values() if v)


# ---------------------------------------------------------------- stages


def pulls_signature(paths):
    return [[f.name, f.stat().st_size, int(f.stat().st_mtime)] for f in sorted(paths.pulls.glob("*.json"))] if paths.pulls.exists() else []


def write_state(paths, args, accounts):
    state = {"today": f"{TODAY:%Y-%m-%d}", "followers": list(args.followers or []), "pulls": pulls_signature(paths),
             "accounts": {h: {"normal": a["normal"], "scores": {p["code"]: p["score"] for p in a["posts"] if p["score"] is not None}}
                          for h, a in accounts.items()}}
    write(paths.state, json.dumps(state, indent=1))


def load_state(paths, args):
    """Every stage after stats uses stats' date (and follower numbers), so normals and scores never drift."""
    global TODAY
    if not paths.state.exists():
        fail("Run stats first: it fixes the date and the normal (middle views) the rest of the study uses.")
    st = read_json(paths.state)
    if args.today and args.today != st["today"]:
        say(f"Using the date stats used ({st['today']}), so the numbers match. To change it, run stats again with --today.")
    TODAY = dt.datetime.fromisoformat(st["today"]).replace(tzinfo=dt.timezone.utc)
    if st.get("pulls") != pulls_signature(paths):
        fail("The pulls changed since stats ran. Run stats again first, so every number comes from the same pull.")
    return st


def stage_stats(args, paths):
    files, accounts = load_accounts(paths, args.followers or ())
    if not accounts:
        fail(f"No Apify pulls found. Save each pull as a .json file in {paths.pulls} and run this again.")
    write_state(paths, args, accounts)
    for h, a in accounts.items():
        write(paths.account(h) / "stats.md", stats_md(a))
    n_thumbs = write_dashboard(paths, accounts, thumbs=not args.no_thumbs)
    say(f"Read {len(files)} pull file(s), {sum(len(a['posts']) for a in accounts.values())} posts, {len(accounts)} accounts.")
    for h, a in accounts.items():
        reach = f", reach {a['reach']:.2f}" if a["reach"] is not None else ", reach not checked (no follower count)"
        say(f"  @{h} ({a['platform']}): normal {fmt(a['normal'])} from {len(a['used'])} videos, "
            f"{plural(a['winners_used'], 'winner')} in those{reach}. Best: "
            + (", ".join(f"{fmt(p['views'])} views (score {score_txt(p)})" for p in a["top"][:3]) or "none"))
    note = f"{n_thumbs} thumbnails" if ffmpeg_exe(required=False) or args.no_thumbs else "no thumbnails: the video tool isn't installed yet"
    say(f"Wrote my-content-team/study/<handle>/stats.md for each account and my-content-team/study/dashboard.html ({note}).")


def stage_pick(args, paths):
    st = load_state(paths, args)
    _, accounts = load_accounts(paths, st.get("followers") or ())
    if not accounts:
        fail("No pulls yet. Run stats first.")
    can = lambda p: p["kind"] == "video" and p.get("video_url") and p["score"] is not None and not p["pinned"] and not p["too_new"]
    picks = []
    if args.codes:
        want = [c.strip() for c in args.codes.split(",") if c.strip()]
        index = {p["code"]: p for a in accounts.values() for p in a["posts"]}
        for c in want:
            if c in index:
                p = index[c]
                picks.append((p, "winner" if (p["score"] or 0) >= WINNER else "normal post for contrast"))
            else:
                say(f"  {c}: not in the pulls, skipped")
    else:
        total = max(1, args.total)
        accs = sorted(accounts.values(), key=lambda a: a["winners_all"], reverse=True)
        if total >= 3 * len(accs):
            contrast = len(accs)  # 1 normal post per account
        else:
            contrast = max(1, round(total / 4)) if total >= 3 else 0
        winners = {a["handle"]: [p for p in sorted(a["scored"], key=lambda p: p["score_raw"], reverse=True) if can(p) and p["score"] >= WINNER]
                   for a in accs}
        for a in accs:  # an account with no single winner: its best videos stand in
            if not winners[a["handle"]]:
                winners[a["handle"]] = [p for p in sorted(a["scored"], key=lambda p: p["score_raw"], reverse=True) if can(p)][:3]
        chosen = []
        while len(chosen) < total - contrast and any(winners.values()):  # winners, taking turns between accounts
            for a in accs:
                if winners[a["handle"]] and len(chosen) < total - contrast:
                    chosen.append((winners[a["handle"]].pop(0), "winner"))
        taken = {id(p) for p, _ in chosen}
        normals = {a["handle"]: sorted([p for p in a["used"] if can(p) and id(p) not in taken],
                                       key=lambda p: abs(p["score_raw"] - 1.0)) for a in accs}
        per_acc = {a["handle"]: 0 for a in accs}
        for _ in range(2):  # then normal posts for contrast: 1 per account first, never more than 2
            for a in accs:
                h = a["handle"]
                if len(chosen) < total and normals[h] and per_acc[h] < 2 and (per_acc[h] == 0 or len(chosen) < total):
                    chosen.append((normals[h].pop(0), "normal post for contrast"))
                    per_acc[h] += 1
        picks = [(p, why if (p["score"] or 0) >= WINNER or why != "winner" else "best of this account (no single winner)") for p, why in chosen]
        n_win = sum(1 for p, _ in picks if (p["score"] or 0) >= WINNER)
        if len(picks) < total:
            say(f"Only {n_win} winner{'' if n_win == 1 else 's'} (2.0 or more) in these pulls, so I picked {len(picks)} reels, not {total}.")
    out = [{"platform": p["platform"], "handle": p["handle"], "code": p["code"], "why": why} for p, why in picks]
    write(paths.picks, json.dumps(out, indent=1))
    say(f"Picked {len(out)} reels (saved in study-tmp/picks.json):")
    for p, why in picks:
        say(f"  @{p['handle']} {p['date']:%Y-%m-%d}: {fmt(p['views'])} views, score {score_txt(p)} ({why}). "
            f"\"{short(p['caption'], 60)}\" [{p['code']}]")


def load_picks(paths, args=None):
    if not paths.picks.exists():
        fail("No reels picked yet. Run: study.py pick --total N")
    st = load_state(paths, args or argparse.Namespace(today=None))
    _, accounts = load_accounts(paths, st.get("followers") or ())
    for h, a in accounts.items():  # belt and braces: the normal is the one stats wrote
        saved = st["accounts"].get(h, {}).get("normal")
        if saved is not None and saved != a["normal"]:
            fail(f"@{h}: the normal changed since stats ({saved} then, {a['normal']} now). Run stats again.")
    index = {(p["platform"], p["code"]): (a, p) for a in accounts.values() for p in a["posts"]}
    out = []
    for x in read_json(paths.picks):
        hit = index.get((x["platform"], x["code"]))
        if hit:
            out.append((hit[0], hit[1], x.get("why", "")))
    return out


def video_path(paths, p):
    return paths.videos / p["handle"] / f"{p['code']}.mp4"


def audio_path(paths, p):
    return paths.videos / p["handle"] / f"{p['code']}.audio.m4a"


def stage_download(args, paths):
    picks = load_picks(paths, args)
    ok = 0
    for a, p, _ in picks:
        v = video_path(paths, p)
        v.parent.mkdir(parents=True, exist_ok=True)
        label = f"@{p['handle']} {p['code']}"
        if v.exists() and v.stat().st_size > 1000:
            say(f"  {label}: already downloaded")
            ok += 1
            continue
        if not p.get("video_url"):
            say(f"  {label}: no video link in the pull (TikTok needs shouldDownloadVideos on). Skipped.")
            continue
        try:
            fetch(p["video_url"], v, timeout=120)
            if v.stat().st_size < 1000:
                raise RuntimeError("the file came back empty")
            mb = v.stat().st_size / 1e6
            if ffmpeg_exe(required=False) and not probe(v)[1] and p.get("audio_url"):
                fetch(p["audio_url"], audio_path(paths, p), timeout=120)
                say(f"  {label}: {mb:.1f} MB (the video had no sound, got the sound file too)")
            else:
                say(f"  {label}: {mb:.1f} MB")
            ok += 1
        except Exception as e:
            if v.exists():
                v.unlink()
            why = "the link has expired, pull this post again" if re.search(r"HTTP Error (403|404|410)", str(e)) else str(e)
            say(f"  {label}: couldn't download ({why})")
    say(f"Downloaded {ok} of {len(picks)} into study-tmp/videos/.")


def stage_transcribe(args, paths):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        rerun_in_venv("The speech-to-text tool (faster-whisper)")
    picks = load_picks(paths, args)
    todo = []
    for a, p, _ in picks:
        out = paths.account(p["handle"]) / "transcripts" / f"{p['code']}.json"
        v = video_path(paths, p)
        if out.exists() and not args.force:
            continue
        if not v.exists():
            say(f"  @{p['handle']} {p['code']}: no video downloaded, skipped")
            continue
        todo.append((p, v, out))
    if not todo:
        say("Nothing new to transcribe.")
        return
    t0 = time.time()
    say(f"Loading the speech model ({args.model}). The first time, this downloads it once.")
    model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=min(4, os.cpu_count() or 2))
    lang = None if args.language == "auto" else args.language
    n_speech = n_none = 0
    for p, v, out in todo:
        ap_ = audio_path(paths, p)
        if not ap_.exists() and p.get("audio_url") and ffmpeg_exe(required=False) and not probe(v)[1]:
            try:  # the video came without sound: Instagram keeps the sound in a separate file
                fetch(p["audio_url"], ap_, timeout=120)
            except Exception:
                pass
        src = ap_ if ap_.exists() else v
        t1 = time.time()
        try:
            segs, info = model.transcribe(str(src), language=lang, beam_size=1, vad_filter=True,
                                          vad_parameters={"min_silence_duration_ms": 500})
            segs = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                     "no_speech_prob": round(s.no_speech_prob, 3)} for s in segs]
        except Exception as e:
            say(f"  @{p['handle']} {p['code']}: couldn't read the sound ({e})")
            continue
        real = [s for s in segs if s["text"] and not HALLU.match(s["text"]) and s["no_speech_prob"] < 0.6]
        secs = sum(s["end"] - s["start"] for s in real)
        words = sum(len(s["text"].split()) for s in real)
        none = secs < 1.5 or words < 4
        rec = {"code": p["code"], "model": args.model, "duration": round(info.duration, 2),
               "no_speech": none, "speech_seconds": round(secs, 2), "segments": [] if none else segs}
        if none:
            rec["discarded"] = segs
            text = "[no speech]"
            n_none += 1
        else:
            text = "\n".join(f"[{s['start']:.1f}s] {s['text']}" for s in segs)
            n_speech += 1
        write(out, json.dumps(rec, indent=1, ensure_ascii=False))
        write(out.with_suffix(".txt"), text + "\n")
        say(f"  @{p['handle']} {p['code']}: {'no speech' if none else str(words) + ' words'} ({time.time() - t1:.0f}s)")
    say(f"Transcribed {n_speech + n_none} reels ({n_none} with no speech) in {time.time() - t0:.0f}s. "
        f"Saved in my-content-team/study/<handle>/transcripts/.")


MEDIA_EXT = (".mp3", ".m4a", ".mp4", ".mov", ".wav", ".aac", ".ogg", ".webm", ".mkv", ".m4v", ".flac", ".aiff")


def source_name(s):  # like safe_name, but keeps hyphens, so the Repurposer's short names survive
    return re.sub(r"[^a-z0-9._-]+", "-", str(s or "").lower()).strip("-.") or "long-piece"


def stage_transcribe_file(args, paths):
    """One long piece for the Repurposer: a local sound or video file, or a direct link to one."""
    if bool(args.file) == bool(args.url):
        fail("Give one of --file \"path/to/file\" or --url \"link to an .mp3 or .m4a\".")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        rerun_in_venv("The speech-to-text tool (faster-whisper)")
    paths.sources.mkdir(parents=True, exist_ok=True)
    if args.file:
        src = Path(args.file).expanduser().resolve()
        if not src.is_file():
            fail(f"I can't find that file: {src}")
        name = source_name(args.name or src.stem)
    else:
        name = source_name(args.name or Path(args.url.split("?")[0]).stem)
        ext = Path(args.url.split("?")[0]).suffix.lower()
        src = paths.sources / f"{name}{ext if ext in MEDIA_EXT else '.media'}"
        if not src.exists():
            req = Request(args.url, headers={"User-Agent": UA})
            try:
                with urlopen(req, timeout=60) as r:
                    kind = (r.headers.get("Content-Type") or "").lower()
                    if kind.startswith("text/html"):
                        fail("That link is a web page, not a sound or video file. "
                             "Look for the episode's Download link (it usually ends in .mp3).")
                    with open(src, "wb") as f:
                        shutil.copyfileobj(r, f)
            except Exception as e:
                if src.exists():
                    src.unlink()
                if isinstance(e, SystemExit):
                    raise
                fail(f"I couldn't download that file ({e}).")
            say(f"Downloaded {src.stat().st_size / 1e6:.1f} MB into study-tmp/sources/.")
    out = paths.sources / f"{name}.txt"
    if out.exists() and not args.force:
        say(f"Already transcribed: study-tmp/sources/{name}.txt (add --force to redo it).")
        return
    t0 = time.time()
    say(f"Loading the speech model ({args.model}). The first time, this downloads it once.")
    model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=min(4, os.cpu_count() or 2))
    lang = None if args.language == "auto" else args.language
    try:
        segs, info = model.transcribe(str(src), language=lang, beam_size=1, vad_filter=True,
                                      vad_parameters={"min_silence_duration_ms": 500})
        rows, next_note = [], 300
        for s in segs:
            rows.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                         "no_speech_prob": round(s.no_speech_prob, 3)})
            if s.end >= next_note:  # long recordings: a sign of life every 5 minutes of sound
                say(f"  ...{int(s.end // 60)} minutes in")
                next_note += 300
    except Exception as e:
        fail(f"I couldn't read the sound in that file ({e}).")
    real = [r for r in rows if r["text"] and not HALLU.match(r["text"]) and r["no_speech_prob"] < 0.6]
    words = sum(len(r["text"].split()) for r in real)
    if words < 4:
        fail("I couldn't hear any speech in that file.")

    def stamp(sec):
        sec = int(sec)
        return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60:02d}:{sec % 60:02d}"

    write(out, "\n".join(f"[{stamp(r['start'])}] {r['text']}" for r in real) + "\n")
    write(out.with_suffix(".json"), json.dumps({"name": name, "source": args.url or str(src), "model": args.model,
                                                "duration": round(info.duration, 2), "segments": real},
                                               indent=1, ensure_ascii=False))
    say(f"Transcribed {info.duration / 60:.1f} minutes ({words} words) in {time.time() - t0:.0f}s. "
        f"Saved in study-tmp/sources/{name}.txt.")


def scene_scores(video):
    out = run([ffmpeg_exe(), "-hide_banner", "-i", video, "-vf",
               "scale=270:-2,select='gte(scene,0)',metadata=print:file=-", "-an", "-f", "null", "-"]).stdout
    rows, t = [], None
    for line in out.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            t = float(m.group(1))
        m = re.search(r"scene_score=([0-9.]+)", line)
        if m and t is not None:
            rows.append((t, float(m.group(1))))
    return rows


def find_cuts(rows):
    """Hard cuts score over 0.3. A jump cut in the same framing scores low but spikes for one frame."""
    hard = [round(t, 2) for t, s in rows if s > 0.3 and t >= 0.2]
    jumps = []
    for i, (t, s) in enumerate(rows):
        nb = [rows[j][1] for j in range(max(0, i - 2), min(len(rows), i + 3)) if j != i]
        if t >= 0.2 and s >= 0.035 and s >= 2.5 * max(nb or [0]) and (not jumps or t - jumps[-1] >= 0.3) \
                and all(abs(t - h) >= 0.3 for h in hard):
            jumps.append(round(t, 2))
    return hard, jumps


def cut_facts(dur, hard, jumps):
    cuts = sorted(hard + jumps)
    bounds = [0.0] + cuts + [dur]
    shots = [round(b - a, 2) for a, b in zip(bounds, bounds[1:]) if b - a > 0]
    return {
        "duration": round(dur, 2), "cut_count": len(cuts), "cut_times": cuts,
        "hard_cuts": hard, "jump_cuts": jumps,
        "note": "found by a tool, so roughly right: hard cuts change the picture, jump cuts keep the same framing",
        "first_cut_at": cuts[0] if cuts else None,
        "cuts_first_3s": sum(c < 3 for c in cuts),
        "cuts_per_10s": round(len(cuts) / dur * 10, 1) if dur else None,
        "average_shot": round(dur / (len(cuts) + 1), 1) if dur else None,
        "longest_shot": max(shots) if shots else None,
    }


def make_frames(video, fd):
    """Hook frames every 0.5s for the first 3s, contact sheets, cuts.json. Returns a short summary."""
    ff = ffmpeg_exe()
    if fd.exists():
        shutil.rmtree(fd)
    fd.mkdir(parents=True)
    dur, _ = probe(video)
    q = ["-hide_banner", "-loglevel", "error", "-y"]
    run([ff] + q + ["-t", "3", "-i", video, "-vf", "fps=2:round=down,scale=540:-2", "-q:v", "4", fd / "tmp-%02d.jpg"])
    for i, f in enumerate(sorted(fd.glob("tmp-*.jpg"))):
        f.rename(fd / f"hook-{i * 0.5:.1f}s.jpg")

    ffl = ffmpeg_exe(required=False, drawtext=True)  # only an ffmpeg that can print text gets to draw the times
    labels = {"done": False}

    def labelled(extra_in, vf, out, single):  # with the time printed on each tile if we can, else plain
        tries = [(ffl, label_filter(16)), (ffl, label_filter(16, font=False))] if ffl else []
        for exe, lab in tries + [(ff, "")]:
            r = run([exe] + q + extra_in + ["-vf", vf.replace("{LABEL}", lab)] + (["-frames:v", "1"] if single else [])
                    + ["-q:v", "4", out])
            if r.returncode == 0 and (out.exists() if single else any(fd.glob("tmp-sec-*.jpg"))):
                labels["done"] = bool(lab)
                return
    labelled(["-t", "3", "-i", video], "fps=2:round=down,scale=240:-2,{LABEL}tile=3x2", fd / "hook.jpg", True)
    hook_labelled = labels["done"]
    # 1 frame per second with its time on it, then 24 to a sheet; the last sheet only as tall as it needs
    labelled(["-i", video], "fps=1:round=down,scale=200:-2,{LABEL}null", fd / "tmp-sec-%03d.jpg", False)
    secs = sorted(fd.glob("tmp-sec-*.jpg"))
    per = 24
    sheet_times = {"hook.jpg": [f"{i * 0.5:.1f}s" for i in range(len(list(fd.glob("hook-*.jpg"))))]}
    for k in range(0, len(secs), per):
        count = min(per, len(secs) - k)
        name = f"seconds-{k // per + 1}.jpg"
        run([ff] + q + ["-framerate", "1", "-start_number", str(k + 1), "-i", fd / "tmp-sec-%03d.jpg",
                        "-vf", f"tile={min(6, count)}x{-(-count // 6)}", "-frames:v", "1", "-q:v", "4", fd / name])
        sheet_times[name] = [f"{k + i}s" for i in range(count)]  # tile i (left to right, top to bottom) = second k + i
    for f in secs:
        f.unlink()
    hard, jumps = find_cuts(scene_scores(video))
    facts = cut_facts(dur, hard, jumps)
    facts["frames"] = {"hook": sorted(f.name for f in fd.glob("hook-*.jpg")),
                       "sheets": ["hook.jpg"] + sorted((f.name for f in fd.glob("seconds-*.jpg")), key=lambda n: int(re.sub(r"\D", "", n) or 0)),
                       "times_printed_on_tiles": bool(hook_labelled and labels["done"]),
                       "tile_times": sheet_times}
    write(fd / "cuts.json", json.dumps(facts, indent=1))
    return facts


def stage_frames(args, paths):
    ffmpeg_exe()
    if not ffmpeg_exe(required=False, drawtext=True):
        say("Note: this computer's video tool can't print the time on each picture, so the contact sheets have no "
            "time labels. Each breakdown lists the time of every tile instead (left to right, top to bottom).")
    picks = load_picks(paths, args)
    t0 = time.time()
    n = 0
    for a, p, _ in picks:
        v = video_path(paths, p)
        fd = paths.account(p["handle"]) / "frames" / p["code"]
        if (fd / "cuts.json").exists() and not args.force:
            continue
        if not v.exists():
            say(f"  @{p['handle']} {p['code']}: no video downloaded, skipped")
            continue
        t1 = time.time()
        f = make_frames(v, fd)
        n += 1
        say(f"  @{p['handle']} {p['code']}: {f['duration']:.0f}s long, {f['cut_count']} cuts, "
            f"{len(f['frames']['sheets'])} contact sheets ({time.time() - t1:.0f}s)")
    say(f"Made frames for {n} reels in {time.time() - t0:.0f}s. Saved in my-content-team/study/<handle>/frames/.")


STUB_SECTIONS = [
    "1. Hook (first 3 seconds)", "2. Words on screen", "3. Shots and setting", "4. Pacing",
    "5. The parts of the video", "6. Call to action", "7. Why it worked (best guess)", "8. Steal this",
    "9. How to make one like it",
]


def stub_text(a, p, why, tr, cuts, fd, rel):
    q = lambda s: '"' + str(s).replace('"', "'").replace("\n", " ") + '"'
    has_speech = None if tr is None else not tr.get("no_speech")
    first = (tr["segments"][0]["text"] if tr and tr.get("segments") else "none (no speech)") if tr else "not transcribed"
    L = ["---", "status: stub",
         "# measured by study.py (keep these lines as they are)",
         f"account: {q('@' + p['handle'])}", f"platform: {p['platform']}", f"code: {q(p['code'])}",
         f"link: {q(p['url'])}", f"posted: {p['date']:%Y-%m-%d}" if p["date"] else "posted: not in the pull",
         f"picked_as: {q(why)}",
         f"views: {int(p['views']) if p['views'] is not None else q('not in the pull')}",
         f"normal: {int(a['normal']) if a['normal'] else q('not in the pull')}",
         f"score: {p['score'] if p['score'] is not None else q('not scored')}",
         f"likes: {int(p['likes']) if p['likes'] is not None else q('not visible')}",
         f"comments: {int(p['comments']) if p['comments'] is not None else q('not visible')}",
         f"shares: {int(p['shares']) if p['shares'] is not None else (q('not in the public data') if p['platform'] == 'Instagram' else q('not visible'))}",
         f"saves: {q('not in the public data') if p['platform'] == 'Instagram' else (int(p['saves']) if p['saves'] is not None else q('not visible'))}",
         f"length_s: {round(p['length'] or (cuts or {}).get('duration') or 0, 1) or q('not in the pull')}",
         f"speech: {q('not transcribed') if has_speech is None else ('yes' if has_speech else 'no')}",
         f"first_line: {q(first)}  # machine heard: check in the hook frames that the creator is the one talking (could be a guest's voice or a clip)",
         f"cuts: {cuts['cut_count'] if cuts else q('not measured')}",
         f"cuts_per_10s: {cuts['cuts_per_10s'] if cuts else q('not measured')}",
         f"music: {q(p.get('music') or 'not in the pull')}",
         "# filled by Claude (words from formats.md)",
         "format: \"\"", "hook_type: \"\"", "topic: \"\"", "cta: \"\"", "---", "",
         f"# @{p['handle']}, {p['date']:%Y-%m-%d}: {fmt(p['views'])} views, score {score_txt(p)}" if p["date"] else f"# @{p['handle']}",
         "", "## 0. Measured facts (made by study.py, keep as is)", "",
         f"- Link: {p['url']}",
         f"- Views {fmt(p['views'])} ÷ normal {fmt(a['normal'])} = score {score_txt(p)}. Picked as: {why}.",
         f"- Likes {fmt(p['likes'])}, comments {fmt(p['comments'])}"
         + ((f", shares {fmt(p['shares'])}, saves not in the public data (Instagram)" if p["shares"] is not None
             else ", shares and saves not in the public data (Instagram)") if p["platform"] == "Instagram"
            else f", shares {fmt(p['shares'])}, saves {fmt(p['saves'])}") + ". All from Apify."]
    if cuts:
        L.append(f"- Length {cuts['duration']:.1f}s. Cuts: {cuts['cut_count']} ({plural(len(cuts['hard_cuts']), 'picture change')}, "
                 f"{plural(len(cuts['jump_cuts']), 'jump cut')}), {cuts['cuts_per_10s']} per 10 seconds, first cut at "
                 f"{str(cuts['first_cut_at']) + 's' if cuts['first_cut_at'] is not None else 'none'}, "
                 f"longest shot {cuts['longest_shot']}s. Found by a tool, so roughly right.")
        L.append(f"- Cut times (seconds): {', '.join(str(c) for c in cuts['cut_times']) or 'none'}")
    else:
        L.append("- Cuts: not measured (no frames yet)")
    L.append(f"- Sound: {p.get('music') or 'not in the pull'} (music info)")
    L += ["", "### Caption", "", "```", (p["caption"] or "").strip() or "(no caption)", "```", "",
          "### What's said, with times (machine heard on this computer)", ""]
    if tr is None:
        L.append("not transcribed yet")
    elif tr.get("no_speech"):
        L.append("[no speech] (music or other sound only)")
    else:
        L += [f"- [{s['start']:.1f}s] {s['text']}" for s in tr["segments"]]
    L += ["", "### Frames to read", ""]
    if cuts:
        fr = cuts["frames"]
        tt = fr.get("tile_times") or {}
        span = lambda n: f"tiles left to right, top to bottom: {tt[n][0]} to {tt[n][-1]}" if tt.get(n) else "left to right"
        L.append("Each tile has its time printed in the corner." if fr.get("times_printed_on_tiles") else
                 "No time is printed on the tiles (this computer's video tool can't): use the times below, never guess.")
        L += [f"- `{rel}/frames/{p['code']}/hook.jpg` (first 3 seconds, every half second; {span('hook.jpg')})"]
        L += [f"- `{rel}/frames/{p['code']}/{s}` (1 frame per second; {span(s)})" for s in fr["sheets"][1:]]
        L += [f"- Full size: `{rel}/frames/{p['code']}/hook-0.0s.jpg` to `hook-2.5s.jpg`"]
    else:
        L.append("- none yet (run the frames stage)")
    L.append("")
    L += [f"## {s}\n" for s in STUB_SECTIONS]
    return "\n".join(L)


def stage_stubs(args, paths):
    picks = load_picks(paths, args)
    made = kept = 0
    for a, p, why in picks:
        d = paths.account(p["handle"])
        out = d / "breakdowns" / f"{p['code']}.md"
        if out.exists():
            old = out.read_text(encoding="utf-8")
            tail = old.split("## 1. Hook", 1)[1] if "## 1. Hook" in old else ""
            filled = any(l.strip() and not l.startswith("## ") for l in tail.splitlines()[1:])
            if not old.startswith("---\nstatus: stub") or filled:
                kept += 1
                continue
        trf = d / "transcripts" / f"{p['code']}.json"
        cf = d / "frames" / p["code"] / "cuts.json"
        tr = read_json(trf) if trf.exists() else None
        cuts = read_json(cf) if cf.exists() else None
        write(out, stub_text(a, p, why, tr, cuts, d / "frames", f"my-content-team/study/{p['handle']}"))
        made += 1
    say(f"Wrote {made} breakdown stubs in my-content-team/study/<handle>/breakdowns/"
        + (f" (left {kept} that Claude already filled in)." if kept else "."))


def stage_cleanup(args, paths):
    if not args.all and paths.sources.exists():
        gone = [f for f in paths.sources.iterdir() if f.suffix.lower() in MEDIA_EXT or f.suffix == ".media"]
        for f in gone:
            f.unlink()
        if gone:
            say(f"Deleted {len(gone)} downloaded sound or video files from study-tmp/sources/. The transcripts stay.")
    target = paths.tmp if args.all else paths.videos
    if not target.exists():
        say("Nothing to delete.")
        return
    files = [f for f in target.rglob("*") if f.is_file()]
    mb = sum(f.stat().st_size for f in files) / 1e6
    shutil.rmtree(target)
    if args.all:
        say(f"Deleted study-tmp/ ({len(files)} files, {mb:.0f} MB): the videos, the pulls and the thumbnails.")
    else:
        say(f"Deleted {len(files)} downloaded video files ({mb:.0f} MB) from study-tmp/videos/. "
            "Transcripts, frames and notes stay in my-content-team/study/.")


# ---------------------------------------------------------------- Apify, straight from this computer

APIFY = "https://api.apify.com/v2"
# Only Actors from apify-actors.md (the team's approved list). Instagram reels come from the official reel scraper.
IG_REEL_ACTOR = "apify~instagram-reel-scraper"
IG_REEL_FIELDS = ("shortCode,url,type,productType,timestamp,videoPlayCount,videoViewCount,likesCount,commentsCount,"
                  "videoDuration,caption,isPinned,ownerUsername,inputUrl,videoUrl,audioUrl,displayUrl,musicInfo,"
                  "sharesCount,shareCount,reshareCount")
TT_FIELDS = ("id,text,createTimeISO,playCount,diggCount,commentCount,shareCount,collectCount,videoMeta,webVideoUrl,"
             "mediaUrls,isPinned,isSlideshow,authorMeta,musicMeta")
# Free plan prices, from the Apify store on 2026-11-04 (they change: apify-actors.md has the date).
PRICE = {"ig_reel": 0.0026, "ig_shares": 0.007, "start": 0.001, "ig_profile": 0.0026, "tt_post": 0.003 + 0.0013}


def token_file():
    return VENV_DIR / ".env"


def apify_token():
    tok = os.environ.get("APIFY_TOKEN", "").strip()
    f = token_file()
    if not tok and f.exists():
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            k, _, v = line.partition("=")
            if k.strip() == "APIFY_TOKEN":
                tok = v.strip().strip('"').strip("'")
    if not tok:
        try:  # make the empty file, so the owner only has to open it and paste
            if not f.exists() and f.parent.exists():
                f.write_text("APIFY_TOKEN=\n", encoding="utf-8")
        except Exception:
            pass
        fail("I can't find your Apify key yet. Open this file, paste your key right after APIFY_TOKEN= and save it:\n"
             f"  {f}\n(If the file isn't there, make it: a plain text file with one line, APIFY_TOKEN=your key.)")
    return tok


def apify(method, path, tok, body=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    req = Request(APIFY + path, data=data, method=method,
                  headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json", "User-Agent": "study.py"})
    try:
        with urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        code = getattr(e, "code", None)
        msg = ""
        try:
            msg = json.loads(e.read().decode("utf-8")).get("error", {}).get("message", "")  # type: ignore[attr-defined]
        except Exception:
            pass
        if code == 401:
            fail("Apify didn't accept the key. Copy it again from Apify (Settings, API & Integrations) into "
                 f"{token_file()} and save.")
        if code == 402 or "credit" in msg.lower() or "limit" in msg.lower():
            fail(f"Apify said no: {msg or 'not enough credit'}. Your free credit may be used up for this month.")
        fail(f"Apify didn't answer as expected ({code or e}). {msg}".strip())


def apify_plan(me):
    return str((me.get("plan") or {}).get("id") or "unknown").upper()


def stage_check_apify(args, paths):
    me = apify("GET", "/users/me", apify_token()).get("data", {})
    plan = apify_plan(me)
    say(f"Apify key works. Signed in as: {me.get('username') or 'unknown'} (Apify plan: {plan.lower()})")
    if plan == "FREE":
        say("Instagram share counts need a paid Apify plan, so on this plan pulls come without them.")


def run_actor(tok, actor, inp, budget, label):
    """Start an Actor with a spending cap, wait for it, return (run, items)."""
    run = apify("POST", f"/acts/{actor}/runs?maxTotalChargeUsd={budget:.2f}", tok, inp).get("data", {})
    rid, t0 = run.get("id"), time.time()
    say(f"  {label}: started on Apify, waiting...")
    while run.get("status") in ("READY", "RUNNING", None) and time.time() - t0 < 900:
        run = apify("GET", f"/actor-runs/{rid}?waitForFinish=60", tok, timeout=90).get("data", {})
    if run.get("status") in ("READY", "RUNNING"):
        fail(f"  {label}: still running after 15 minutes. Check it on apify.com, then run this again.")
    last = None
    for _ in range(8):  # Apify fills in the cost over a few seconds after the run ends: wait until it stops moving
        time.sleep(3)
        run = apify("GET", f"/actor-runs/{rid}", tok).get("data", {})
        now = (run.get("usageTotalUsd"), json.dumps(run.get("chargedEventCounts"), sort_keys=True))
        if now == last and (now[0] or 0) > 0:
            break
        last = now
    return run


def run_cost(run):
    """What the run cost: Apify's own total, or else its charged events at the free plan price."""
    if (run.get("usageTotalUsd") or 0) > 0:
        return float(run["usageTotalUsd"]), "Apify"
    events = (run.get("pricingInfo") or {}).get("pricingPerEvent", {}).get("actorChargeEvents", {})
    total = 0.0
    for name, count in (run.get("chargedEventCounts") or {}).items():
        e = events.get(name, {})
        price = e.get("eventPriceUsd") or (e.get("eventTieredPricingUsd") or {}).get("FREE", {}).get("tieredEventPriceUsd") or 0
        total += (count or 0) * price
    if run.get("chargedEventCounts"):
        return total, "worked out from the charged events"
    return (0.0, "Apify") if run.get("usageTotalUsd") == 0 else (None, None)


def dataset_items(tok, run, fields):
    ds = run.get("defaultDatasetId")
    if not ds:
        return []
    out, offset = [], 0
    while True:
        page = apify("GET", f"/datasets/{ds}/items?clean=true&format=json&limit=1000&offset={offset}&fields={fields}", tok)
        items = page if isinstance(page, list) else page.get("data", page.get("items", []))
        out += items
        if len(items) < 1000:
            return out
        offset += 1000


def stage_pull(args, paths):
    ig = [safe_name(h) for h in (args.instagram or "").split(",") if h.strip()]
    tt = [safe_name(h) for h in (args.tiktok or "").split(",") if h.strip()]
    if not ig and not tt:
        fail("Say which accounts: --instagram handle1,handle2 and/or --tiktok handle1,handle2")
    n = max(1, args.posts)
    # shares are a paid add-on: on by default for a normal pull, off for a long one unless the owner said yes
    shares = args.shares if args.shares is not None else n <= 30
    per_reel = PRICE["ig_reel"] + (PRICE["ig_shares"] if shares else 0)
    est = len(ig) * (n * per_reel + PRICE["start"] + PRICE["ig_profile"]) + len(tt) * n * PRICE["tt_post"]
    budget = args.budget if args.budget else round(est * 1.3 + 0.05, 2)
    if budget < est:
        say(f"Note: the cap ${budget:.2f} is under the estimate ${est:.2f}, so some posts may not come back.")
    tok = apify_token()
    paths.pulls.mkdir(parents=True, exist_ok=True)
    if ig and shares:
        try:
            plan = apify_plan(apify("GET", "/users/me", tok).get("data", {}))
        except SystemExit:
            plan = "unknown"
        if plan == "FREE":  # the shares add-on is for paid Apify plans only: it would send nothing
            say("Instagram share counts need a paid Apify plan, and this one is free, so this pull goes without them.")
            shares = False
            per_reel = PRICE["ig_reel"]
            est = len(ig) * (n * per_reel + PRICE["start"] + PRICE["ig_profile"]) + len(tt) * n * PRICE["tt_post"]
            if not args.budget:
                budget = round(est * 1.3 + 0.05, 2)
    try:  # Apify quietly lowers a run's cap to the credit left this month, so check first
        lim = apify("GET", "/users/me/limits", tok).get("data", {})
        left_month = (lim.get("limits") or {}).get("maxMonthlyUsageUsd", 0) - (lim.get("current") or {}).get("monthlyUsageUsd", 0)
    except SystemExit:
        left_month = None
    if left_month is not None and left_month < 0.005:
        fail("Your Apify credit for this month is used up, so Apify won't run anything. A fresh $5 arrives at the start "
             "of your next Apify month. Until then: screenshots of the grid, or the posts already pulled.")
    if left_month is not None and left_month < est:
        say(f"Heads up: you have about ${left_month:.2f} of Apify credit left this month and this pull needs about "
            f"${est:.2f}, so Apify will stop early and fewer posts will come back.")
    say(f"Pulling {n} posts from {len(ig) + len(tt)} account(s)"
        + (f", Instagram shares {'on' if shares else 'off'}" if ig else "")
        + f". Estimate about ${est:.2f}, spending cap ${budget:.2f}.")
    t0, spent, left = time.time(), 0.0, budget
    ig_input = {"resultsLimit": n, "includeSharesCount": bool(shares), "skipTrialReels": False}
    if n > 30:  # a long pull: up to n reels or one year back, whichever comes first (the Actor's own date filter)
        ig_input["onlyPostsNewerThan"] = "12 months"
    jobs = [(IG_REEL_ACTOR, dict(ig_input, username=[h]), IG_REEL_FIELDS, h, "",
             n * per_reel + PRICE["start"]) for h in ig]
    jobs += [("clockworks~tiktok-profile-scraper", {"profiles": [h], "resultsPerPage": n, "shouldDownloadVideos": True,
              "shouldDownloadCovers": False, "shouldDownloadSubtitles": False}, TT_FIELDS, h, "", n * PRICE["tt_post"]) for h in tt]
    if ig and not args.no_profile:
        jobs.append(("apify~instagram-profile-scraper", {"usernames": ig}, "username,followersCount", None, "-profile",
                     len(ig) * PRICE["ig_profile"]))
    for actor, inp, fields, h, suffix, job_est in jobs:
        label = f"@{h}" if h else "follower counts"
        cap = round(min(left, job_est * 1.5 + 0.02), 2)
        if cap < 0.01:
            say(f"  {label}: skipped, the spending cap is used up.")
            continue
        run = run_actor(tok, actor, inp, cap, label)
        items = dataset_items(tok, run, fields)
        cost, how = run_cost(run)
        if cost is not None:
            spent += cost
            left = max(0.0, budget - spent)
        status = run.get("status")
        got_cap = (run.get("options") or {}).get("maxTotalChargeUsd")
        if isinstance(got_cap, (int, float)) and got_cap < cap - 0.001:
            say(f"  {label}: Apify lowered the spending cap from ${cap:.2f} to ${got_cap:.2f} (your credit left this "
                "month), so this run stopped early.")
        if actor == IG_REEL_ACTOR and inp.get("includeSharesCount") and items and \
                not any(any(k in i for k in ("sharesCount", "shareCount", "reshareCount")) for i in items):
            say(f"  @{h}: Apify sent no share counts (charged shares: {(run.get('chargedEventCounts') or {}).get('shares-count', 0)}). "
                "On Apify's free plan the shares add-on is switched off: it needs a paid plan (Starter or higher). "
                "Shares stay 'not in the public data' for this account.")
        if h and len(items) < n:
            dates = sorted(filter(None, (parse_date(i.get("timestamp") or i.get("createTimeISO")) for i in items)))
            back = f", back to {dates[0]:%Y-%m-%d}" if dates else ""
            if n > 30 and dates and (dates[-1] - dates[0]).days >= 350:
                say(f"  @{h}: {len(items)} posts cover a full year{back}, so that's all of them for the year.")
            else:
                say(f"  @{h}: asked for {n} posts, Apify returned {len(items)}{back}.")
        if h:
            write(paths.pulls / f"{h}.json", json.dumps(items, indent=1, ensure_ascii=False))
            say(f"  @{h}: {len(items)} posts saved to study-tmp/pulls/{h}.json ({status}"
                + (f", cost ${cost:.4f}, {how}" if cost is not None else ", cost not shown by Apify") + ")")
        else:
            for it in items:
                hh = safe_name(it.get("username"))
                write(paths.pulls / f"{hh}{suffix}.json", json.dumps([it], indent=1, ensure_ascii=False))
            say(f"  follower counts: {len(items)} profile(s) saved ({status}"
                + (f", cost ${cost:.4f}, {how}" if cost is not None else ", cost not shown by Apify") + ")")
    say(f"Done in {time.time() - t0:.0f}s. Apify cost this pull: ${spent:.4f}. Next: stats.")


def stage_plan(args, paths):
    f = Path.home() / ".claude.json"
    name = tier = None
    try:
        acct = json.loads(f.read_text(encoding="utf-8")).get("oauthAccount") or {}
        name, tier = acct.get("planDisplayName"), acct.get("organizationRateLimitTier")
    except Exception:
        pass
    say(f"planDisplayName: {name or 'not found'}")
    say(f"organizationRateLimitTier: {tier or 'not found'}")
    t, n = (str(tier or "")).lower(), (str(name or "")).lower()
    if "20x" in t or "20x" in n:
        hint = "looks like Max 20x or higher: about 15 reels"
    elif "5x" in t or "5x" in n:
        hint = "looks like Max 5x: about 10 reels"
    elif "pro" in t or re.search(r"\bpro\b", n):
        hint = "looks like Pro: about 5 to 6 reels"
    else:
        hint = "can't tell: ask the owner which plan they're on"
    say(f"suggestion: {hint}")


def stage_selftest(args, paths):
    say(f"Python {sys.version.split()[0]} at {sys.executable}")
    if sys.version_info < (3, 9):
        fail("This needs Python 3.9 or newer.")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        rerun_in_venv("The speech-to-text tool (faster-whisper)")
    ff = ffmpeg_exe()
    say(f"Video tool: {ff}")
    t0 = time.time()
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        speech = None
        if shutil.which("say"):  # Mac: a real spoken line
            r = run(["say", "-o", td / "s.aiff", "Testing the study tools. One, two, three, four, five."])
            speech = td / "s.aiff" if r.returncode == 0 else None
        audio_in = ["-i", speech] if speech else ["-f", "lavfi", "-i", "sine=frequency=440:duration=4"]
        r = run([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc=duration=2:size=360x640:rate=25",
                 "-f", "lavfi", "-i", "color=c=red:duration=2:size=360x640:rate=25"] + audio_in +
                ["-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]", "-map", "2:a", "-shortest",
                 "-pix_fmt", "yuv420p", td / "test.mp4"])
        if r.returncode:
            fail("The video tool couldn't make a test clip:\n" + r.stderr[-800:])
        facts = make_frames(td / "test.mp4", td / "frames")
        cut_ok = any(abs(c - 2.0) < 0.2 for c in facts["cut_times"])
        say(f"Frames: {len(facts['frames']['hook'])} hook frames, {len(facts['frames']['sheets'])} contact sheets, "
            f"cut found at 2.0s: {'yes' if cut_ok else 'no'}")
        t1 = time.time()
        model = WhisperModel(args.model, device="cpu", compute_type="int8")
        segs, _ = model.transcribe(str(td / "test.mp4"), language="en", beam_size=1, vad_filter=True)
        text = " ".join(s.text.strip() for s in segs)
        if speech:
            heard_ok = bool(re.search(r"test|three|four|five", text, re.I))
            say(f"Speech: heard \"{text.strip()}\" ({time.time() - t1:.0f}s with model {args.model})")
        else:
            heard_ok = True
            say(f"Speech: model {args.model} loaded and ran on a test tone ({time.time() - t1:.0f}s)")
    if facts["frames"]["hook"] and heard_ok:
        say(f"Self-test passed in {time.time() - t0:.0f}s. The study tools work on this computer.")
    else:
        fail("Self-test didn't pass. Send this whole message to Claude.")


def stage_setup(args, paths):
    if sys.version_info < (3, 9):
        fail(f"This computer's Python is {sys.version.split()[0]}. The study tools need 3.9 or newer.")
    req = HERE / "requirements.txt"
    vp = venv_python()
    if not vp:
        say(f"Making a private tools folder at {VENV_DIR} (only the study tools go in it)...")
        r = subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)])
        vp = venv_python()
        if r.returncode or not vp:
            fail("Couldn't make the tools folder. On Linux, install python3-venv first.")
    say("Installing faster-whisper and imageio-ffmpeg (about 260 MB, plus about 150 MB for the speech model, a few minutes)...")
    subprocess.run([str(vp), "-m", "pip", "install", "--quiet", "--upgrade", "pip"])
    r = subprocess.run([str(vp), "-m", "pip", "install", "--quiet", "-r", str(req)])
    if r.returncode:
        fail("The install didn't finish. Check the internet connection and run setup again.")
    env_file = VENV_DIR / ".env"
    if not env_file.exists():
        env_file.write_text("APIFY_TOKEN=\n", encoding="utf-8")  # the owner pastes their Apify key here later
    say("Installed. Running the self-test (the first run downloads the speech model once)...")
    env = dict(os.environ, STUDY_IN_VENV="1", KMP_DUPLICATE_LIB_OK="TRUE")
    sys.exit(subprocess.call([str(vp), str(Path(__file__).resolve()), "selftest", "--model", args.model], env=env))


# ---------------------------------------------------------------- main


def main():
    global TODAY
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["plan", "setup", "selftest", "check-apify", "pull", "stats", "pick", "download", "transcribe", "transcribe-file",
                                      "frames", "stubs", "cleanup"])
    ap.add_argument("--root", default=".", help="the owner's working folder (default: this folder)")
    ap.add_argument("--today", help="today's date as YYYY-MM-DD (the owner's date wins)")
    ap.add_argument("--followers", action="append", help="handle=number, when the pull has no follower count")
    ap.add_argument("--no-thumbs", action="store_true", help="stats: don't fetch thumbnails")
    ap.add_argument("--total", type=int, default=5, help="pick: how many reels in all")
    ap.add_argument("--codes", help="pick: exactly these posts, comma separated")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"transcribe: speech model (default {DEFAULT_MODEL}; small.en is slower and more exact)")
    ap.add_argument("--language", default="en", help="transcribe: language code, or auto")
    ap.add_argument("--instagram", help="pull: Instagram handles, comma separated")
    ap.add_argument("--tiktok", help="pull: TikTok handles, comma separated")
    ap.add_argument("--posts", type=int, default=30, help="pull: posts per account (30, or 250 for a year)")
    ap.add_argument("--budget", type=float, help="pull: the most Apify may charge for this pull, in dollars")
    ap.add_argument("--no-profile", action="store_true", help="pull: skip the Instagram follower counts")
    ap.add_argument("--shares", dest="shares", action="store_true", default=None,
                    help="pull: add Instagram share counts (paid add-on; on by default for 30 or fewer posts)")
    ap.add_argument("--no-shares", dest="shares", action="store_false", help="pull: no Instagram share counts")
    ap.add_argument("--file", help="transcribe-file: a sound or video file on this computer")
    ap.add_argument("--url", help="transcribe-file: a direct link to a sound or video file (e.g. a podcast .mp3)")
    ap.add_argument("--name", help="transcribe-file: a short name for the transcript (default: the file's name)")
    ap.add_argument("--force", action="store_true", help="redo work already on disk")
    ap.add_argument("--all", action="store_true", help="cleanup: delete all of study-tmp/")
    args = ap.parse_args()
    TODAY = today_utc(args)
    paths = Paths(args.root)
    os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    globals()[f"stage_{args.stage.replace('-', '_')}"](args, paths)


if __name__ == "__main__":
    main()
