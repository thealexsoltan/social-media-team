#!/usr/bin/env python3
"""
Full account breakdown: the Data Analyst's dashboard tool.

The dashboard page is ONE file: ../assets/dashboard-template.html (the IG profile
dashboard page, used as it is). This script never rebuilds it. It only:
  1. copies the template and puts the owner's saved pull into its empty
     <script type="application/json" id="ownerdata"> block, so the page opens
     straight on their numbers (the page's own code does every sum, as always);
  2. prints a short summary for the chat (worked out with the same rules as the
     page), the comparison with the last pull, and rows for results-log.md.

Run it from the owner's working folder (the folder that holds my-content-team/):

  python3 dashboard.py my-content-team/analytics/2026-11-04-instagram.json
      writes my-content-team/analytics/dashboard.html and prints the summary

  options:
    --out PATH          where to write the page (default: dashboard.html next to the pull)
    --previous PATH     the pull to compare against (default: the newest older
                        *-instagram.json in the same folder; "none" to skip)
    --today YYYY-MM-DD  the owner's date (default: the pull date)
    --check             only read the pull and say what's in it and what's missing
    --no-open           don't open the page in the browser afterwards (also skipped when CI is set)

  without Composio, from an Instagram content export (CSV):
    python3 dashboard.py --from-csv export.csv --save-json my-content-team/analytics/2026-11-04-instagram.json
      reads the export into the same JSON shape (account totals stay empty: an
      export has none), saves it, then builds the page from it

What it reads: the aicc-ig-v3 block from references/full-breakdown.md (the shape the
page itself reads), or a recorded raw pull {"calls": [...]} (the page reads that too).

Python 3.8 or newer, nothing to install, no network.
"""
import argparse
import os
import csv
import datetime as dt
import glob
import json
import math
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

SCHEMA = "aicc-ig-v3"  # the id the page validates; kept as is
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "dashboard-template.html"
SLOT = '<script type="application/json" id="ownerdata"></script>'
DAY = 86400.0
REEL_CAP = 60
WIN_KEYS = ["views", "reach", "accounts_engaged", "total_interactions", "likes", "comments", "shares", "saves",
            "replies", "reposts", "profile_views", "website_clicks", "follows", "reach_follower", "reach_non_follower",
            "views_follower", "views_non_follower", "views_unknown"]
TOT_METRICS = WIN_KEYS[:12]
AUD = ["follower", "engaged", "reached"]
DIMS = ["age", "gender", "country", "city"]
AUD_METRIC = {"follower": "follower_demographics", "engaged": "engaged_audience_demographics",
              "reached": "reached_audience_demographics"}

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass


# ---------------------------------------------------------------- helpers

def rhu(x, nd=0):
    if x is None:
        return None
    q = Decimal(str(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return int(q) if nd == 0 else float(q)


def num(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v if math.isfinite(v) else None
    if isinstance(v, str):
        s = re.sub(r"[,\s%$€£]", "", v)
        try:
            x = float(s) if s else None
        except ValueError:
            return None
        return None if x is None else (int(x) if x.is_integer() else x)
    return None


def nn(v):
    v = num(v)
    return None if v is None or v < 0 else v


def parse_ts(s):
    if s is None or s == "":
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        s += "T00:00:00Z"
    s = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", s)
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    if re.search(r"T\d{2}:\d{2}\+", s):
        s = s.replace("+", ":00+", 1)
    d = None
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        for f in ("%m/%d/%Y %H:%M", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"):
            try:
                d = dt.datetime.strptime(s.split("+")[0], f)
                break
            except ValueError:
                pass
    if d is None:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.timestamp()


def iso_day(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%d")


def add_days(day, n):
    return iso_day(parse_ts(day) + n * DAY)


def median(a):
    s = sorted(x for x in a if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x))
    n = len(s)
    if not n:
        return None
    return s[(n - 1) // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def n0(x):
    return "not given" if x is None else f"{rhu(x):,}"


def f1(x, d=1):
    return "not given" if x is None else f"{rhu(x, d):,.{d}f}"


def pct(x, d=1):
    return "not given" if x is None else f"{rhu(x, d):.{d}f}%"


def first_line(c):
    s = str(c or "").split("\n")[0].strip()
    return re.sub(r"\s+\S*$", "", s[:79]) + "…" if len(s) > 80 else s


# ---------------------------------------------------------------- reading a recorded raw pull (same rules as the page's fromComposio)

UI, MI = "INSTAGRAM_GET_USER_INSIGHTS", "INSTAGRAM_GET_IG_MEDIA_INSIGHTS"


def key_of(slug, a):
    a = a or {}
    if slug == "INSTAGRAM_GET_USER_INFO":
        return "profile"
    if slug == "INSTAGRAM_GET_IG_USER_MEDIA":
        return "media"
    m = a.get("metric") or []
    m = m if isinstance(m, list) else [m]
    if slug == MI:
        return ("skip:" if "reels_skip_rate" in m else "reel:") + str(a.get("ig_media_id"))
    span = ""
    if a.get("since") and a.get("until") and parse_ts(a["since"]) is not None and parse_ts(a["until"]) is not None:
        span = str(round((parse_ts(a["until"]) - parse_ts(a["since"])) / DAY))
    name, bd = ",".join(m), a.get("breakdown") or ""
    if name == "follower_count":
        return "fc"
    if name == "online_followers":
        return "online"
    for who, met in AUD_METRIC.items():
        if name == met:
            return f"demo:{who}:{bd}"
    if span in ("28", "7"):
        if name == "follows_and_unfollows":
            return "follows" + span
        if bd == "follow_type":
            return ("reachft" if name == "reach" else "viewsft") + span
        if not bd:
            return "totals" + span
    return f"{slug}:{name}|{bd}|{span}"


def ins_list(r):
    return r["data"]["data"] if r and r.get("ok") and isinstance(r.get("data"), dict) and isinstance(r["data"].get("data"), list) else None


def find_m(lst, name):
    return next((x for x in lst or [] if isinstance(x, dict) and x.get("name") == name), None)


def tv_of(lst, name):
    m = find_m(lst, name)
    tv = m.get("total_value") if m else None
    return nn(tv.get("value")) if isinstance(tv, dict) else None


def arms_of(lst, name):
    m = find_m(lst, name)
    tv = m.get("total_value") if m else None
    b = (tv.get("breakdowns") or [None])[0] if isinstance(tv, dict) else None
    if b and b.get("results"):
        return {str(x["dimension_values"][0]): nn(x.get("value")) for x in b["results"] if x.get("dimension_values")}
    return None


def from_calls(raw):
    by = {}
    for c in raw.get("calls") or []:
        r = c.get("response") or {}
        by[c.get("key") or key_of(c.get("tool_slug"), c.get("arguments"))] = (
            {"ok": False, "error": r.get("error") or "failed"} if r.get("successful") is False else {"ok": True, "data": r.get("data")})
    missing = []
    miss = lambda m, why: missing.append({"metric": m, "reason": why})
    fail_why = lambda r: ("Instagram or Composio refused it: " + str(r.get("error"))[:140]) if r and r.get("error") else "not pulled"
    P = by.get("profile", {}).get("data") if by.get("profile", {}).get("ok") else None
    if isinstance(P, dict) and isinstance(P.get("data"), dict) and not P.get("username"):
        P = P["data"]
    fol = nn(P.get("followers_count")) if P else None
    acct = {"username": P.get("username") if P else None, "name": P.get("name") if P else None,
            "account_type": P.get("account_type") if P else None, "followers": fol,
            "following": nn(P.get("follows_count")) if P else None, "media_count": nn(P.get("media_count")) if P else None}
    if not P:
        miss("profile", fail_why(by.get("profile")))
    small = "no" if fol is None else "under_100" if fol < 100 else "under_1000" if fol < 1000 else "no"
    pulled = raw.get("pulled_at") or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = raw.get("today") or iso_day(parse_ts(pulled))
    windows = {}
    for k in ("28", "7"):
        o = {"since": add_days(today, -int(k)), "until": today}
        T = ins_list(by.get("totals" + k))
        for m in TOT_METRICS:
            o[m] = tv_of(T, m) if T else None
        if not T and by.get("totals" + k):
            miss(f"account totals ({k} days)", fail_why(by["totals" + k]))
        fa = arms_of(ins_list(by.get("follows" + k)), "follows_and_unfollows") or {}
        o["follows"] = fa.get("FOLLOWER")
        if o["follows"] is None and by.get("follows" + k):
            miss(f"follows ({k} days)", "Instagram returned no breakdown")
        rf = arms_of(ins_list(by.get("reachft" + k)), "reach") or {}
        vf = arms_of(ins_list(by.get("viewsft" + k)), "views") or {}
        o.update(reach_follower=rf.get("FOLLOWER"), reach_non_follower=rf.get("NON_FOLLOWER"),
                 views_follower=vf.get("FOLLOWER"), views_non_follower=vf.get("NON_FOLLOWER"), views_unknown=vf.get("UNKNOWN"))
        if any(o.get(m) is not None for m in WIN_KEYS):
            windows[k] = o
    daily = None
    fm = find_m(ins_list(by.get("fc")), "follower_count")
    if fm and fm.get("values"):
        daily = []
        for i, v in enumerate(fm["values"]):
            t, val = parse_ts(v.get("end_time")), nn(v.get("value"))
            if i == len(fm["values"]) - 1 and val == 0:
                val = None
            if t is not None:
                daily.append({"date": iso_day(t - DAY), "value": val})
    elif by.get("fc"):
        miss("follower_count", "Instagram hides it under 100 followers" if small == "under_100" else "Instagram returned no values")
    online = None
    ol = find_m(ins_list(by.get("online")), "online_followers")
    if ol and isinstance(ol.get("values"), list):
        online = []
        for v in ol["values"]:
            t, h = parse_ts(v.get("end_time")), v.get("value") if isinstance(v.get("value"), dict) else {}
            hours = [nn(h.get(str(i))) for i in range(24)]
            if t is not None and any(x is not None for x in hours):
                online.append({"date": iso_day(t - DAY), "hours": hours})
        if not online:
            online = None
            miss("online_followers", "Instagram returned no hours")
    demo = {}
    for who in AUD:
        demo[who] = {b: arms_of(ins_list(by.get(f"demo:{who}:{b}")), AUD_METRIC[who]) for b in DIMS}
        if not any(demo[who].values()) and by.get(f"demo:{who}:age"):
            miss(AUD_METRIC[who], "Instagram hides it under 100 followers" if small == "under_100" else "Instagram returned no breakdown")
    reels = []
    md = by.get("media", {}).get("data") if by.get("media", {}).get("ok") else None
    ml = md if isinstance(md, list) else (md.get("data") if isinstance(md, dict) and isinstance(md.get("data"), list) else
                                          md["data"].get("data") if isinstance(md, dict) and isinstance(md.get("data"), dict) else None)
    if ml:
        rl = sorted([m for m in ml if m and m.get("id") and m.get("media_type") == "VIDEO" and m.get("media_product_type") in (None, "REELS")],
                    key=lambda m: parse_ts(m.get("timestamp")) or 0, reverse=True)[:REEL_CAP]
        no_ins = 0
        for m in rl:
            ins, sk = ins_list(by.get("reel:" + str(m["id"]))), ins_list(by.get("skip:" + str(m["id"])))

            def v(name):
                x = find_m(ins, name)
                return nn(x["values"][0].get("value")) if x and x.get("values") else None
            sv = find_m(sk, "reels_skip_rate")
            aw, t = v("ig_reels_avg_watch_time"), parse_ts(m.get("timestamp"))
            no_ins += 0 if ins else 1
            reels.append({"id": str(m["id"]), "permalink": m.get("permalink"),
                          "posted": dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if t else None,
                          "feed": m.get("is_shared_to_feed") if isinstance(m.get("is_shared_to_feed"), bool) else None,
                          "hook": first_line(m.get("caption")), "views": v("views"), "reach": v("reach"),
                          "likes": v("likes") if ins else nn(m.get("like_count")), "comments": v("comments") if ins else nn(m.get("comments_count")),
                          "saves": v("saved"), "shares": v("shares"), "interactions": v("total_interactions"),
                          "avg_watch_s": rhu(aw / 1000, 1) if aw is not None else None,
                          "skip_rate": nn(sv["values"][0].get("value")) if sv and sv.get("values") else None, "insights": bool(ins)})
        if no_ins:
            miss("reel insights", f"{no_ins} of {len(reels)} reels had none" + (" (Instagram gives reel insights from about 1,000 followers)" if small != "no" else ""))
    elif by.get("media"):
        miss("media", fail_why(by.get("media")))
    return {"schema": SCHEMA, "pulled_at": pulled, "source": "composio", "account": acct, "windows": windows, "daily_follows": daily,
            "online_followers": online, "demographics": demo, "reels": reels, "status": {"small_account": small}, "missing": missing}


# ---------------------------------------------------------------- one clean shape (same rules as the page's cleanV3)

def clean(d):
    notes = []
    if not isinstance(d, dict):
        return None, notes, ['This file is not a pull. It should start with {"schema":"aicc-ig-v3".']
    if isinstance(d.get("calls"), list) and not d.get("schema"):
        d = from_calls(d)
        notes.append("read a recorded raw pull")
    if d.get("schema") != SCHEMA:
        return None, notes, [f'This file says it is "{str(d.get("schema"))[:40]}". The dashboard reads the aicc-ig-v3 block from references/full-breakdown.md.']
    a = d.get("account") or {}
    out = {"pulled_at": d.get("pulled_at") if parse_ts(d.get("pulled_at")) is not None else None, "source": str(d.get("source") or "unknown"),
           "account": {"username": str(a["username"]).lstrip("@") if a.get("username") else None, "name": a.get("name"),
                       "account_type": a.get("account_type"), "followers": nn(a.get("followers")),
                       "following": nn(a.get("following")), "media_count": nn(a.get("media_count"))}, "windows": {}}
    for k, w in (d.get("windows") or {}).items():
        w = w or {}
        o = {"since": str(w["since"])[:10] if w.get("since") else None, "until": str(w["until"])[:10] if w.get("until") else None}
        for m in WIN_KEYS:
            o[m] = nn(w.get(m))
        days = round((parse_ts(o["until"]) - parse_ts(o["since"])) / DAY) if o["since"] and o["until"] else None
        o["days"] = days if days and days > 0 else num(k)
        if o["days"] and any(o[m] is not None for m in WIN_KEYS):
            out["windows"][str(int(o["days"]))] = o
    reels = []
    for r in d.get("reels") or []:
        if not isinstance(r, dict) or r.get("id") is None or parse_ts(r.get("posted")) is None:
            continue
        reels.append({"id": str(r["id"]), "posted": dt.datetime.fromtimestamp(parse_ts(r["posted"]), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "feed": r["feed"] if isinstance(r.get("feed"), bool) else None, "hook": str(r.get("hook") or "")[:120],
                      **{k: nn(r.get(k)) for k in ("views", "reach", "likes", "comments", "saves", "shares", "interactions", "avg_watch_s",
                                                   "skip_rate", "follows", "profile_visits", "link_taps")},
                      "insights": False if r.get("insights") is False else nn(r.get("views")) is not None})
    reels.sort(key=lambda r: parse_ts(r["posted"]), reverse=True)
    out["reels"] = reels
    f = out["account"]["followers"]
    st = (d.get("status") or {}).get("small_account")
    out["status"] = {"small_account": st if st in ("under_100", "under_1000", "no") else
                     "no" if f is None else "under_100" if f < 100 else "under_1000" if f < 1000 else "no"}
    out["missing"] = [{"metric": str(x.get("metric") or "unknown"), "reason": str(x.get("reason") or "Instagram would not give it")} if isinstance(x, dict)
                      else {"metric": str(x), "reason": "Instagram would not give it"} for x in d.get("missing") or []]
    if out["pulled_at"] is None:
        out["pulled_at"] = reels[0]["posted"] if reels else dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        notes.append("no pull date in the file, so the newest reel's date was used")
    if not out["windows"] and not reels and f is None:
        return None, notes, ["The file has no numbers in it. Run the pull again."]
    return out, notes, []


# ---------------------------------------------------------------- the page's sums, for the chat summary (ported from its engine)

def ibeta(x, a, b):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))

    def cf(a, b, x):
        FP, qab, qap, qam = 1e-300, a + b, a + 1, a - 1
        c, d = 1.0, 1 - qab * x / qap
        d = 1 / (d if abs(d) > FP else FP)
        h = d
        for m in range(1, 5001):
            m2 = 2 * m
            for aa in (m * (b - m) * x / ((qam + m2) * (a + m2)), -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))):
                d = 1 + aa * d
                d = 1 / (d if abs(d) > FP else FP)
                c = 1 + aa / c
                c = c if abs(c) > FP else FP
                de = d * c
                h *= de
            if abs(de - 1) < 3e-14:
                break
        return h
    return bt * cf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * cf(b, a, 1 - x) / b


def jeffreys(x, n):
    if not n or n <= 0 or x is None or x < 0 or x > n:
        return None

    def q(p, a, b):
        lo, hi = 0.0, 1.0
        for _ in range(80):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if ibeta(m, a, b) < p else (lo, m)
        return (lo + hi) / 2
    return (0.0 if x == 0 else q(0.025, x + .5, n - x + .5), 1.0 if x == n else q(0.975, x + .5, n - x + .5))


STEPS = [dict(key="interaction", name="Interaction rate", lo=4, hi=6, bench="4 to 6%", mult=100, xn="interactions"),
         dict(key="profile", name="Profile visit rate", lo=3, hi=10, bench="3 to 10%", mult=100, xn="profile visits"),
         dict(key="linktap", name="Link tap rate", lo=1, hi=3, bench="1 to 3%", mult=100, xn="taps"),
         dict(key="follows", name="Follows per 1,000 reach", lo=5, hi=10, bench="5 to 10", mult=1000, xn="follows")]
HEAD = {"interaction": ("People watch your reels, but hardly anyone likes, comments, shares or saves them.", "Ask one simple question in each reel that people can answer in a comment."),
        "profile": ("People watch your reels, but very few tap your name to see who made them.", 'End each reel with one clear reason to visit your profile, for example "part 2 is on my page".'),
        "linktap": ("People open your profile, but very few tap the link in your bio.", "Make the first line of your bio say, in plain words, what people get when they tap the link."),
        "follows": ("People see your reels, but very few follow you.", 'Tell people what they get by following, for example "follow for part 2".')}


def band(v, lo, hi):
    return "exceptional" if v >= 2 * hi else "strong" if v > hi else "on" if v >= lo else "near" if v >= .8 * lo else "below" if v >= .5 * lo else "critical"


def funnel(w):
    T = w or {}
    reach_used = bool(T.get("reach"))
    src = {"interaction": (T.get("total_interactions"), T.get("views")),
           "profile": (T.get("profile_views"), T.get("reach") if reach_used else T.get("views")),
           "linktap": (T.get("website_clicks"), T.get("profile_views")), "follows": (T.get("follows"), T.get("reach"))}
    steps = []
    for s in STEPS:
        x, n = src[s["key"]]
        o = dict(s, num=x, den=n, value=None, status="none", chip="none")
        if x is not None and n:
            v = o["value"] = x / n * s["mult"]
            o["ratio"] = v / s["lo"]
            o["status"] = o["chip"] = "data" if x > n else band(v, s["lo"], s["hi"])
            if o["status"] != "data":
                floor = s["lo"] / s["mult"]
                E = .01 if floor >= .01 else floor / 2
                o["need"] = math.ceil(1.959964 ** 2 * floor * (1 - floor) / (E * E))
                ci = jeffreys(x, n)
                if ci and ci[0] <= floor <= ci[1] and n < o["need"]:
                    o["chip"] = "noread"
        steps.append(o)
    cands = sorted([s for s in steps if s["value"] is not None and s["chip"] != "noread" and s["status"] != "data" and s["ratio"] < 1 and s["den"] >= 30],
                   key=lambda s: s["ratio"])
    return {"steps": steps, "by": {s["key"]: s for s in steps}, "bottleneck": cands[0] if cands else None, "reach_used": reach_used}


def sv(s):
    return f1(s["value"], 1) if s["mult"] == 1000 else pct(s["value"], 1 if s["value"] >= 100 else 2)


def readings(F):
    W, N = [], []
    for s in F["steps"]:
        if s["value"] is None:
            continue
        line = f"{s['name']}: {sv(s)} against {s['bench']}{' per 1,000' if s['mult'] == 1000 else ''} ({n0(s['num'])} {s['xn']} from {n0(s['den'])})."
        if s["status"] == "data":
            N.append((1.5, f"{s['name']} looks off: {n0(s['num'])} from {n0(s['den'])}, more than is possible. Read the steps after it loosely."))
        elif s["chip"] == "noread":
            N.append((1.4, f"Too few people to judge {s['name'].lower()} yet: {n0(s['den'])}, about {n0(s['need'])} needed."))
        elif s["status"] in ("exceptional", "strong"):
            W.append((2 + min(2, s["value"] / s["hi"] - 1), line))
        elif s["status"] == "on":
            W.append((1, line))
        else:
            b = s is F["bottleneck"]
            N.append((10 if b else 1 + min(2, 1 / s["ratio"] - 1), line + (" This is the bottleneck." if b else "")))
    return [t for _, t in sorted(W, key=lambda x: -x[0])][:3], [t for _, t in sorted(N, key=lambda x: -x[0])][:3]


def reel_stats(D):
    if not D["reels"]:
        return {"available": False}
    now = parse_ts(D["pulled_at"])
    allr = []
    for r in D["reels"]:
        t = parse_ts(r["posted"])
        allr.append(dict(r, t=t, age=(now - t) / DAY, published=r["feed"] is not False,
                         sane=r["views"] is not None and (r["likes"] is None or r["likes"] <= r["views"])))
    basis = "views" if any(r["views"] is not None for r in allr) else "likes"
    metric = lambda r: r[basis]
    pub = [r for r in allr if r["published"]]
    settled = [r for r in pub if r["age"] >= 3 and (r["sane"] if basis == "views" else r["likes"] is not None)]
    base = settled[:30]
    med = median([metric(r) for r in base])
    for r in allr:
        r["vi"] = metric(r) / med if metric(r) is not None and med else None
        r["score"] = rhu(r["vi"], 1) if r["vi"] is not None else None
    win = [r for r in base if r["vi"] is not None and r["vi"] >= 3 and r["skip_rate"] is not None]
    rest = [r for r in base if r["vi"] is not None and r["vi"] < 3 and r["skip_rate"] is not None]
    return {"available": True, "basis": basis, "reels": pub, "trial": [r for r in allr if not r["published"]], "base": base, "med": med,
            "n_base": len(base), "normal_ok": len(base) >= 9, "n_young": len([r for r in pub if r["age"] < 3]),
            "n3": len([r for r in base if r["vi"] and r["vi"] >= 3]), "n5": len([r for r in base if r["vi"] and r["vi"] >= 5]),
            "n2": len([r for r in base if r["score"] is not None and r["score"] >= 2.0]), "nflop": len([r for r in base if r["score"] is not None and r["score"] < 0.5]),
            "skip": median([r["skip_rate"] for r in base]), "skip_win": median([r["skip_rate"] for r in win]) if len(win) >= 2 else None,
            "skip_rest": median([r["skip_rate"] for r in rest]) if len(rest) >= 5 else None,
            "per_week": len([r for r in pub if 0 <= r["age"] <= 28]) / 4}


def analyse(D):
    return {"D": D, "F": {k: funnel(w) for k, w in D["windows"].items()}, "RS": reel_stats(D)}


# ---------------------------------------------------------------- against the last pull

def compare(cur, prev):
    if not prev:
        return None
    D1, D0 = cur["D"], prev["D"]
    gap = (parse_ts(D1["pulled_at"]) - parse_ts(D0["pulled_at"])) / DAY
    rows = [("Followers", D0["account"]["followers"], D1["account"]["followers"], "n")]
    key = "28" if "28" in D1["windows"] and "28" in D0["windows"] else None
    if key:
        w0, w1 = D0["windows"][key], D1["windows"][key]
        for lab, k in (("Views", "views"), ("Reach", "reach"), ("Profile visits", "profile_views"), ("Bio link taps", "website_clicks"),
                       ("Follows gained", "follows"), ("Interactions", "total_interactions"), ("Shares", "shares"), ("Saves", "saves")):
            rows.append((f"{lab} (28 days)", w0.get(k), w1.get(k), "n"))
        for k in ("interaction", "profile", "linktap", "follows"):
            s0, s1 = prev["F"][key]["by"][k], cur["F"][key]["by"][k]
            rows.append((f"{s1['name']} (28 days)", s0["value"], s1["value"], "per1k" if s1["mult"] == 1000 else "pct"))
    R0, R1 = prev["RS"], cur["RS"]
    if R0.get("available") and R1.get("available"):
        rows += [("Normal reel (median views of the last 30)", R0["med"], R1["med"], "n"), ("Reels at 3x or more", R0["n3"], R1["n3"], "n"),
                 ("Reels per week", R0["per_week"], R1["per_week"], "f"), ("Skip rate", R0["skip"], R1["skip"], "pct")]
    return {"date": D0["pulled_at"][:10], "gap": gap, "rows": rows, "overlap": bool(key) and gap < 28}


def fmt_kind(v, kind):
    return "not given" if v is None else pct(v, 2) if kind == "pct" else f1(v, 1) if kind in ("per1k", "f") else n0(v)


def change(a, b, kind):
    if a is None or b is None:
        return ""
    d = b - a
    if kind == "n":
        return f"{'+' if d >= 0 else ''}{rhu(d):,}" + (f" ({'+' if d >= 0 else ''}{rhu(d / a * 100)}%)" if a else "")
    return f"{'+' if d >= 0 else ''}{rhu(d, 2) if kind == 'pct' else rhu(d, 1)}{' points' if kind == 'pct' else ''}"


# ---------------------------------------------------------------- rows for results-log.md (team rules)

def log_rows(D, RS, today):
    if not RS.get("available"):
        return []
    rows, seen = [], set()
    normal = str(rhu(RS["med"])) if RS["med"] and RS["normal_ok"] else "not reliable yet"
    stop = {"a", "an", "the", "and", "or", "of", "to", "is", "it", "in", "on", "for", "you", "your", "i", "my", "this", "that", "with", "at", "be"}
    for r in sorted(RS["reels"], key=lambda r: r["t"]):
        day = r["posted"][:10]
        words = [w for w in re.findall(r"[a-z0-9]+", re.sub(r"['’]", "", r["hook"].lower())) if w not in stop][:4] or ["reel"]
        name, i = f"{day}-{'-'.join(words)}", 2
        while name in seen:
            name, i = f"{day}-{'-'.join(words)}-{i}", i + 1
        seen.add(name)
        score = "too new" if r["age"] < 3 else "no normal yet" if not RS["normal_ok"] else (f1(r["score"], 1) if r["score"] is not None else "not given")
        v = lambda x: "not given" if x is None else str(rhu(x))
        rows.append([name, day, today, str(max(0, rhu((parse_ts(today) - parse_ts(day)) / DAY))), "Instagram", "not known", "not known",
                     v(r["views"]), v(r["likes"]), v(r["comments"]), v(r["shares"]), v(r["saves"]), v(r.get("follows")),
                     v(r.get("profile_visits")), v(r.get("link_taps")), normal, score, r["hook"]])
    return rows


def summary(cur, cmp_, rows, notes, out):
    D, RS = cur["D"], cur["RS"]
    L = ["=" * 60, f"FULL ACCOUNT BREAKDOWN for @{D['account']['username'] or 'unknown'}, pulled {D['pulled_at'][:10]} ({D['source']})", f"Page: {out}"]
    L += [f"Note: {n}" for n in notes]
    key = "28" if "28" in D["windows"] else next(iter(D["windows"]), None)
    if key:
        F = cur["F"][key]
        W, N = readings(F)
        L.append(f"\nWINDOW: last {key} days ({D['windows'][key]['since']} to {D['windows'][key]['until']}), the page's default view")
        L.append("WORKING (top 3):")
        L += [f"  {i}. {t}" for i, t in enumerate(W, 1)] or ["  none on target"]
        L.append("NOT WORKING (top 3, most important first):")
        L += [f"  {i}. {t}" for i, t in enumerate(N, 1)] or ["  nothing below its benchmark"]
        b = F["bottleneck"]
        if b:
            L.append(f"FIX FIRST (the page's primary bottleneck): {HEAD[b['key']][0]} {n0(b['num'])} {b['xn']} from {n0(b['den'])} = {sv(b)}, benchmark {b['bench']}. Try this week: {HEAD[b['key']][1]}")
        else:
            L.append("FIX FIRST: no step with enough people is below its benchmark (the page says so too).")
    else:
        L.append("\nNO ACCOUNT TOTALS: the funnel steps on the page stay empty (export file, or Instagram gave none).")
    if RS.get("available"):
        b = RS["basis"]
        L.append(f"\nREELS: normal (median of the last {RS['n_base']} published reels at least 3 days old) = {n0(RS['med'])} {b}"
                 + ("" if RS["normal_ok"] else "  [under 9: not reliable yet, say 'did a lot better/worse than your others', never winner/flop]"))
        sc = sorted([r for r in RS["base"] if r["score"] is not None], key=lambda r: -r["score"])
        if sc:
            for tag, r in (("best", sc[0]), ("worst", sc[-1])):
                L.append(f"  {tag}: {r['posted'][:10]} \"{r['hook'][:60]}\": {n0(r[b])} ÷ {n0(RS['med'])} = {f1(r['score'], 1)}")
        L.append(f"  2.0 or more (team winners): {RS['n2']} of {RS['n_base']}; under 0.5 (team flops): {RS['nflop']}; 3x or more: {RS['n3']}; 5x or more: {RS['n5']}")
        L.append(f"  {RS['n_young']} still growing (under 3 days), {len(RS['trial'])} trial reels kept out")
        if RS["skip_win"] is not None and RS["skip_rest"] is not None:
            L.append(f"  skip rate: reels at 3x or more {pct(RS['skip_win'], 0)}, the rest {pct(RS['skip_rest'], 0)}")
    if cmp_:
        L.append(f"\nAGAINST YOUR LAST PULL ({cmp_['date']}, {f1(cmp_['gap'], 0)} days ago)" + (f": the 28 day windows share {f1(28 - cmp_['gap'], 0)} days, so changes look smaller than they are" if cmp_["overlap"] else ""))
        L += [f"  {lab}: {fmt_kind(a, k)} -> {fmt_kind(b_, k)}  {change(a, b_, k)}" for lab, a, b_, k in cmp_["rows"] if a is not None or b_ is not None]
    else:
        L.append("\nAGAINST YOUR LAST PULL: this is the first pull, nothing to compare yet")
    if D["missing"]:
        L.append("\nNOT GIVEN (write 'not given', never 0):")
        L += [f"  {m['metric']}: {m['reason']}" for m in D["missing"]]
    if rows:
        L.append("\nROWS FOR results-log.md (swap Post for the plan's short name when it's in content-plan.md; Format and Hook type from the card or formats.md;")
        L.append("a Composio pull has no follows, profile visits or link taps for each reel, so those say 'not given'; an export may have them):")
        L.append("| Post | Posted | Checked | Days old | Platform | Format | Hook type | Views | Likes | Comments | Shares | Saves | Follows | Profile visits | Link taps | Normal | Score |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        L += ["| " + " | ".join(r[:17]) + " |" for r in rows]
        L.append("First caption lines, for matching to the plan:")
        L += [f"  {r[0]}: {r[17]}" for r in rows]
    L.append("=" * 60)
    return "\n".join(L)


# ---------------------------------------------------------------- an export file into the same shape

CSV_COLS = {"posted": ["publish time", "published", "date posted", "created", "post time", "date"], "hook": ["description", "caption", "title", "text"],
            "type": ["post type", "media type", "type"], "views": ["views", "plays", "video views"], "reach": ["reach", "accounts reached"],
            "likes": ["likes", "reactions"], "comments": ["comments"], "shares": ["shares"], "saves": ["saves", "saved", "favourites"],
            "follows": ["follows", "new followers", "followers gained"], "profile_visits": ["profile visits", "profile activity", "profile views"],
            "link_taps": ["link clicks", "website taps", "external link taps", "sticker taps"], "permalink": ["permalink", "link", "url"],
            "id": ["post id", "id", "media id"], "username": ["account username", "username", "account name"]}


def from_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return None, ["The export file is empty."]
    heads = {h.lower().strip(): h for h in rows[0] if h}
    col = {}
    for k, names in CSV_COLS.items():
        hit = next((n for n in names if n in heads), None)
        if hit:
            col[k] = heads[hit]
    if "posted" not in col:
        return None, ["The export has no date column (Publish time or similar), so the posts can't be put in order."]
    reels, other = [], 0
    for i, r in enumerate(rows):
        typ = (r.get(col.get("type"), "") or "").lower()
        if typ and not any(w in typ for w in ("reel", "video")):
            other += 1
            continue
        t = parse_ts(r.get(col["posted"]))
        if t is None:
            continue
        g = lambda k: nn(r.get(col[k])) if k in col else None
        pl = r.get(col["permalink"]) if "permalink" in col else None
        reels.append({"id": (r.get(col["id"]) if "id" in col else None) or f"row{i + 1}",
                      "permalink": pl if pl and re.match(r"^https://(www\.)?instagram\.com/", pl) else None,
                      "posted": dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "feed": True,
                      "hook": first_line(r.get(col["hook"]) if "hook" in col else ""), "views": g("views"), "reach": g("reach"),
                      "likes": g("likes"), "comments": g("comments"), "saves": g("saves"), "shares": g("shares"), "interactions": None,
                      "avg_watch_s": None, "skip_rate": None, "follows": g("follows"), "profile_visits": g("profile_visits"),
                      "link_taps": g("link_taps"), "insights": g("views") is not None})
    missing = [{"metric": k, "reason": "not a column in the export"} for k in ("views", "likes", "comments", "shares", "saves", "reach") if k not in col]
    missing += [{"metric": "account totals", "reason": "an export has numbers for each post only"},
                {"metric": "skip rate and watch time", "reason": "not in the export"},
                {"metric": "audience and followers online", "reason": "not in the export"}]
    if other:
        missing.append({"metric": "photo and carousel posts", "reason": f"{other} left out, the dashboard reads reels and videos only"})
    user = ((rows[0].get(col["username"]) or "").strip() or None) if "username" in col else None
    data = {"schema": SCHEMA, "pulled_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "export",
            "account": {"username": user, "name": None, "account_type": None, "followers": None, "following": None, "media_count": None},
            "windows": {}, "daily_follows": None, "online_followers": None, "demographics": {w: {b: None for b in DIMS} for w in AUD},
            "reels": reels, "status": {"small_account": "no"}, "missing": missing}
    return data, [f"read {len(reels)} reels and videos from the export" + (f", left out {other} photo or carousel posts" if other else "")]


# ---------------------------------------------------------------- main

def load(path):
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return None, None, [], [f"Can't find {path}."]
    except json.JSONDecodeError as e:
        return None, None, [], [f"{path} isn't valid JSON ({e.msg} at line {e.lineno}). Save the pull again in full."]
    D, notes, errors = clean(raw)
    return raw, D, notes, errors


def find_previous(cur_path, cur_t):
    best = None
    for p in glob.glob(str(Path(cur_path).resolve().parent / "*-instagram.json")):
        if Path(p).resolve() == Path(cur_path).resolve():
            continue
        _, D, _, err = load(p)
        t = parse_ts(D["pulled_at"]) if D else None
        if not err and t is not None and t < cur_t - 3600 and (best is None or t > best[0]):
            best = (t, p, D)
    return (best[1], best[2]) if best else (None, None)


def write_page(raw, out):
    page = TEMPLATE.read_text(encoding="utf-8")
    if page.count(SLOT) != 1:
        sys.exit(f"The template at {TEMPLATE} has no empty ownerdata block. Reinstall the skill.")
    blob = json.dumps(raw, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(page.replace(SLOT, f'<script type="application/json" id="ownerdata">{blob}</script>'), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pull", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--previous")
    ap.add_argument("--today")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--from-csv")
    ap.add_argument("--save-json")
    a = ap.parse_args()
    notes = []
    if a.from_csv:
        data, n = from_csv(a.from_csv)
        if data is None:
            sys.exit("Couldn't read the export: " + " ".join(n))
        if a.today:
            data["pulled_at"] = a.today + "T12:00:00Z"  # the owner's date: the day the export was taken
        target = a.save_json or a.pull
        if not target:
            sys.exit("Say where to save it: --save-json my-content-team/analytics/YYYY-MM-DD-instagram.json")
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        Path(target).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        notes += n + [f"saved the export as {target}"]
        a.pull = target
    if not a.pull:
        ap.print_help()
        sys.exit(1)
    raw, D, n, errors = load(a.pull)
    notes += n
    if errors:
        sys.exit("Couldn't read the pull:\n  " + "\n  ".join(errors))
    if a.check:
        print(f"Read @{D['account']['username'] or 'unknown'}: {len(D['reels'])} reels, windows {sorted(D['windows'])}, "
              f"followers {n0(D['account']['followers'])}, source {D['source']}, pulled {D['pulled_at']}.")
        for m in D["missing"]:
            print(f"Not given: {m['metric']}: {m['reason']}")
        return
    cur = analyse(D)
    prev = None
    if (a.previous or "").lower() != "none":
        if a.previous:
            _, P, _, perr = load(a.previous)
            ppath = a.previous
            if perr:
                notes.append(f"couldn't read the last pull: {perr[0]}")
                P = None
        else:
            ppath, P = find_previous(a.pull, parse_ts(D["pulled_at"]))
        if P:
            prev = analyse(P)
            notes.append(f"compared with the last pull {ppath}")
    out = a.out or str(Path(a.pull).resolve().parent / "dashboard.html")
    write_page(raw, out)
    print(summary(cur, compare(cur, prev), log_rows(D, cur["RS"], a.today or D["pulled_at"][:10]), notes, out))
    print(open_page(out, a.no_open))


def open_page(out, no_open=False):
    """Open the finished page in the owner's default browser (Mac and Windows), like double-clicking it."""
    if no_open or os.environ.get("CI"):
        return f"BROWSER: not opened (--no-open or CI). The page is at {Path(out).resolve()}"
    try:
        import webbrowser
        if webbrowser.open(Path(out).resolve().as_uri()):
            return f"BROWSER: opened {Path(out).resolve()} in the default browser"
    except Exception:
        pass
    return f"BROWSER: couldn't open it. The page is at {Path(out).resolve()}"


if __name__ == "__main__":
    main()
