#!/usr/bin/env python3
"""Social Media Team: the computer-side tools, tested the way a new buyer's machine meets them.

What it covers (the only parts of the team that run code on the buyer's computer):
  Content Researcher  study.py   setup (private tools folder), selftest, transcribe-file (the Repurposer's
                                 long-piece route), then a study of two made-up accounts: stats, pick,
                                 download, transcribe, frames, stubs
  Data Analyst        dashboard.py  a made-up Composio pull (plus a comparison with an older pull), --check,
                                    and the no-Composio route from an Instagram export (CSV)

No spend and no accounts: no Apify, no Composio, no keys. The only downloads are the free tools and the
speech model that setup fetches for every buyer. Every account, post and number in ci/fixtures/ is made up.
The test clip is a generated test picture with the computer's own voice (macOS say, Windows speech).

Runs on GitHub's Windows, Intel Mac and Apple Silicon machines (.github/workflows/team-e2e.yml), and by hand:
    python3 ci/e2e.py
Settings (environment):
    E2E_OUT           where the results go (default ci/out); uploaded as the CI artifact
    STUDY_TOOLS_DIR   the private tools folder setup makes (default: a folder in the system temp, never ~/study-tools)
Prints one block per step, then a summary; writes summary.json; exits 1 at the first failed step.
Standard library only.
"""
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PLUGIN = REPO / "social-media-team"
STUDY = PLUGIN / "skills" / "content-researcher" / "scripts" / "study.py"
DASH = PLUGIN / "skills" / "data-analyst" / "scripts" / "dashboard.py"
FIX = HERE / "fixtures"
IS_WIN = os.name == "nt"
OUT = Path(os.environ.get("E2E_OUT") or HERE / "out").resolve()
WORK = OUT / "work"  # the buyer's working folder: my-content-team/ and study-tmp/ land here
TOOLS = Path(os.environ.get("STUDY_TOOLS_DIR") or Path(tempfile.gettempdir()) / "social-media-team-e2e" / "study-tools").resolve()
PY = sys.executable  # the Python a buyer would type: not on the PATH the tools see in CI
TODAY = "2026-10-30"  # the made-up pulls are dated around this day
SENTENCE = "Three easy ways to keep your sourdough starter happy this week."
HEARD = re.compile(r"sourdough|starter|happy|easy|week", re.I)

ENV = dict(os.environ, STUDY_TOOLS_DIR=str(TOOLS), PYTHONIOENCODING="utf-8",
           HF_HOME=str(TOOLS / "model-cache"))  # keep the speech model with the test's tools, not in the home folder
ENV.pop("STUDY_IN_VENV", None)

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

STARTED = time.time()
STEPS = []


def note(text=""):
    print(text, flush=True)


def stamp():
    return f"{time.time() - STARTED:6.0f}s"


def record(name, passed, detail=""):
    STEPS.append({"step": name, "passed": bool(passed), "detail": detail})
    note(f"[{'PASS' if passed else 'FAIL'}] {name}" + (f"  ({detail})" if detail and not passed else ""))
    if not passed:
        done()


def sh(name, args, expect=(), cwd=None, timeout=1800):
    """Run one command, show its output, and pass only on exit 0 with every expected pattern in the output."""
    note(f"\n=== {name}  [{stamp()}]")
    note("    " + " ".join(f'"{a}"' if " " in str(a) else str(a) for a in args))
    try:
        p = subprocess.run([str(a) for a in args], cwd=str(cwd or WORK), env=ENV, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout)
        text, code = (p.stdout or "") + (p.stderr or ""), p.returncode
    except (OSError, subprocess.SubprocessError) as e:
        text, code = f"{type(e).__name__}: {e}", -1
    shown = [l for l in text.splitlines() if l.strip()]
    note("\n".join("    | " + l for l in shown[-60:]))
    (OUT / "logs").mkdir(parents=True, exist_ok=True)
    (OUT / "logs" / (re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".txt")).write_text(text, encoding="utf-8")
    missing = [pat for pat in expect if not re.search(pat, text)]
    record(name, code == 0 and not missing, f"exit {code}" + (f", missing /{missing[0]}/" if missing else ""))
    return text


def check(name, cond, detail=""):
    record(name, cond, detail)


def read(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def done():
    passed = bool(STEPS) and all(s["passed"] for s in STEPS)
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"passed": passed, "os": platform.platform(), "machine": platform.machine(),
               "python": sys.version.split()[0], "seconds": round(time.time() - STARTED), "steps": STEPS}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    note("\n" + "-" * 60)
    for s in STEPS:
        note(f"  {'ok ' if s['passed'] else 'BAD'}  {s['step']}")
    note(f"\n{'PASSED' if passed else 'FAILED'}: {sum(s['passed'] for s in STEPS)} of {len(STEPS)} steps, "
         f"{summary['seconds']}s, {summary['os']} ({summary['machine']}), Python {summary['python']}")
    sys.exit(0 if passed else 1)


def venv_python():
    for p in (TOOLS / "Scripts" / "python.exe", TOOLS / "bin" / "python"):
        if p.exists():
            return p
    return None


def make_voice(dest_base):
    """The computer's own voice saying SENTENCE. Returns the file it made."""
    if IS_WIN:
        dest = dest_base.with_suffix(".wav")
        ps = ("Add-Type -AssemblyName System.Speech; "
              "$v = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              f"$v.SetOutputToWaveFile('{dest}'); $v.Speak('{SENTENCE}'); $v.Dispose()")
        sh("make the test voice (Windows speech)", ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps])
    else:
        dest = dest_base.with_suffix(".aiff")
        sh("make the test voice (macOS say)", ["say", "-o", dest, SENTENCE])
    check("the test voice file exists", dest.exists() and dest.stat().st_size > 10_000, str(dest))
    return dest


def main():
    note(f"Social Media Team e2e on {platform.platform()} ({platform.machine()}), Python {sys.version.split()[0]} at {PY}")
    note(f"results: {OUT}\ntools:   {TOOLS}")
    if OUT.exists():
        shutil.rmtree(OUT)
    WORK.mkdir(parents=True)
    media = OUT / "media"
    media.mkdir()

    # 0. A fresh buyer's machine: no ffmpeg or Node on the PATH (CI hides them). Locally this is only reported.
    seen = {t: shutil.which(t) for t in ("ffmpeg", "node")}
    note(f"on the PATH: {seen}")
    if os.environ.get("CI"):
        check("ffmpeg and Node are hidden from the PATH", not any(seen.values()), str(seen))
    check("the plugin's two scripts are in the repo", STUDY.is_file() and DASH.is_file(), f"{STUDY}, {DASH}")

    # 1. Content Researcher: the one-time install, as Team Setup runs it, then the 10 second check on its own
    if TOOLS.exists():
        shutil.rmtree(TOOLS)
    sh("study.py setup (first run, empty tools folder)", [PY, STUDY, "setup"],
       expect=[r"Making a private tools folder", r"Self-test passed"], timeout=3000)
    check("setup made the tools folder and the empty key file",
          venv_python() is not None and (TOOLS / ".env").is_file() and read(TOOLS / ".env").strip() == "APIFY_TOKEN=")
    sh("study.py selftest (with the buyer's Python, finds the tools folder by itself)", [PY, STUDY, "selftest"],
       expect=[r"Self-test passed", r"cut found at 2\.0s: yes"], timeout=900)

    # The video tool the study tools installed (nothing on the PATH)
    ff = subprocess.run([str(venv_python()), "-c", "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"],
                        capture_output=True, text=True, env=ENV).stdout.strip()
    check("the bundled video tool is there", bool(ff) and Path(ff).exists(), ff or "not found")

    # 2. Test media: a voice, a long-piece sound file, and a 6 second reel with one cut at 3.0s and the voice on it
    voice = make_voice(media / "voice")
    talk = media / "talk.m4a"
    sh("make the long-piece sound file", [ff, "-hide_banner", "-loglevel", "error", "-y", "-i", voice, "-c:a", "aac", talk])
    reel = media / "reel.mp4"
    sh("make the test reel (test picture, cut at 3s, the voice)",
       [ff, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "testsrc=duration=3:size=360x640:rate=25",
        "-f", "lavfi", "-i", "color=c=0x2f6db5:duration=3:size=360x640:rate=25",
        "-i", voice,
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v];[2:a]apad,atrim=0:6[a]",
        "-map", "[v]", "-map", "[a]", "-t", "6", "-pix_fmt", "yuv420p", "-c:a", "aac", reel])
    check("the test reel exists", reel.exists() and reel.stat().st_size > 20_000)

    # 3. Repurposer route: one long piece into words, on this computer
    sh("study.py transcribe-file (one long piece)", [PY, STUDY, "transcribe-file", "--file", talk, "--name", "ci-talk"],
       expect=[r"Transcribed .* words", r"study-tmp/sources/ci-talk\.txt"], timeout=900)
    src_txt = WORK / "study-tmp" / "sources" / "ci-talk.txt"
    check("the long piece's words were heard", src_txt.exists() and bool(HEARD.search(read(src_txt))),
          read(src_txt)[:200] if src_txt.exists() else "no file")
    check("the long piece has a timed .json too", (WORK / "study-tmp" / "sources" / "ci-talk.json").exists())

    # 4. A study of two made-up accounts from saved pulls (what Claude saves after an Apify pull)
    pulls = WORK / "study-tmp" / "pulls"
    pulls.mkdir(parents=True)
    for f in sorted((FIX / "pulls").glob("*.json")):
        shutil.copy2(f, pulls / f.name)
    sh("study.py stats", [PY, STUDY, "stats", "--today", TODAY, "--no-thumbs"],
       expect=[r"Read 2 pull file\(s\), 26 posts, 2 accounts", r"@ci_demo_groomer \(Instagram\): normal 1,030",
               r"@ci_demo_plumber \(TikTok\): normal 1,430"])
    study = WORK / "my-content-team" / "study"
    for h in ("ci_demo_groomer", "ci_demo_plumber"):
        check(f"stats.md for @{h}", (study / h / "stats.md").exists() and "1," in read(study / h / "stats.md"))
    dash_html = study / "dashboard.html"
    check("the study dashboard page", dash_html.exists() and "Account study" in read(dash_html)
          and "ci_demo_plumber" in read(dash_html) and "__DATA__" not in read(dash_html))

    sh("study.py pick", [PY, STUDY, "pick", "--total", "3"], expect=[r"Picked 3 reels"])
    picks = json.loads(read(WORK / "study-tmp" / "picks.json"))
    check("pick chose 2 winners and 1 normal post", len(picks) == 3
          and sum(p["why"] == "winner" for p in picks) == 2, json.dumps(picks))

    # The pulls' video links are made up and never fetched: the reels are put where download leaves them.
    for p in picks:
        dest = WORK / "study-tmp" / "videos" / p["handle"] / f"{p['code']}.mp4"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(reel, dest)
    sh("study.py download (already there, nothing fetched)", [PY, STUDY, "download"],
       expect=[r"already downloaded", r"Downloaded 3 of 3"])
    sh("study.py transcribe (the picked reels)", [PY, STUDY, "transcribe"],
       expect=[r"Transcribed 3 reels \(0 with no speech\)"], timeout=900)
    sh("study.py frames", [PY, STUDY, "frames"], expect=[r"Made frames for 3 reels"], timeout=900)
    sh("study.py stubs", [PY, STUDY, "stubs"], expect=[r"Wrote 3 breakdown stubs"])
    for p in picks:
        acc = study / p["handle"]
        tr = acc / "transcripts" / f"{p['code']}.txt"
        check(f"{p['code']}: transcript heard the voice", tr.exists() and bool(HEARD.search(read(tr))),
              read(tr)[:200] if tr.exists() else "no file")
        fd = acc / "frames" / p["code"]
        cuts = json.loads(read(fd / "cuts.json")) if (fd / "cuts.json").exists() else {}
        check(f"{p['code']}: frames, contact sheets and the cut at 3s",
              (fd / "hook.jpg").exists() and (fd / "seconds-1.jpg").exists() and (fd / "hook-0.0s.jpg").exists()
              and any(abs(c - 3.0) < 0.25 for c in cuts.get("cut_times", [])), json.dumps(cuts.get("cut_times")))
        stub = acc / "breakdowns" / f"{p['code']}.md"
        body = read(stub) if stub.exists() else ""
        check(f"{p['code']}: breakdown stub with the measured facts",
              body.startswith("---\nstatus: stub") and "score: " in body and "speech: yes" in body
              and bool(HEARD.search(body)) and "## 9. How to make one like it" in body
              and "Cut times (seconds):" in body, body[:300])

    # 5. Data Analyst: the full account breakdown from a made-up Composio pull, compared with an older pull
    analytics = WORK / "my-content-team" / "analytics"
    analytics.mkdir(parents=True)
    cur = analytics / f"{TODAY}-instagram.json"
    shutil.copy2(FIX / "composio-pull.json", cur)
    older = json.loads(read(FIX / "composio-pull.json"))
    older["pulled_at"], older["today"] = "2026-10-23T12:00:00Z", "2026-10-23"
    for c in older["calls"]:
        if c["tool_slug"] == "INSTAGRAM_GET_USER_INFO":
            c["response"]["data"]["followers_count"] = 4080
    (analytics / "2026-10-23-instagram.json").write_text(json.dumps(older), encoding="utf-8")

    sh("dashboard.py --check", [PY, DASH, cur, "--check"],
       expect=[r"Read @ci_demo_bakery: 12 reels, windows \['28', '7'\], followers 4,210, source composio",
               r"Not given: reached_audience_demographics"])
    sh("dashboard.py (Composio pull, compared with the last pull)", [PY, DASH, cur],
       expect=[r"FULL ACCOUNT BREAKDOWN for @ci_demo_bakery, pulled 2026-10-30 \(composio\)",
               r"FIX FIRST", r"REELS: normal .* = 2,075 views",
               r"AGAINST YOUR LAST PULL \(2026-10-23", r"Followers: 4,080 -> 4,210",
               r"\| 2026-09-18-scoring-patterns-beginners \|"])
    page = analytics / "dashboard.html"
    html = read(page) if page.exists() else ""
    check("the breakdown page has the pull inside it",
          '<script type="application/json" id="ownerdata">{' in html and "ci_demo_bakery" in html,
          f"{page} ({len(html)} chars)")

    csv_dir = WORK / "csv-route"
    sh("dashboard.py --from-csv (Instagram export, no Composio)",
       [PY, DASH, "--from-csv", FIX / "instagram-export.csv", "--save-json", csv_dir / "2026-10-31-instagram.json",
        "--today", "2026-10-31", "--previous", "none"],
       expect=[r"read 10 reels and videos from the export, left out 1 photo", r"pulled 2026-10-31 \(export\)",
               r"NO ACCOUNT TOTALS", r"REELS: normal"])
    check("the export route saved the JSON and the page",
          (csv_dir / "2026-10-31-instagram.json").exists() and (csv_dir / "dashboard.html").exists())
    done()


if __name__ == "__main__":
    main()
