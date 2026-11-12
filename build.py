#!/usr/bin/env python3
"""Build elenaspatel.com: read data/*.yaml, render templates/*.html into _site/.

Usage:  python3 build.py            (writes _site/)
        python3 -m http.server -d _site 8000   (preview at http://localhost:8000)
"""
import datetime as dt
import hashlib
import pathlib
import shutil

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "_site"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]


def load(name):
    with open(ROOT / "data" / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def sortkey(item):
    """Dates are 'YYYY', 'YYYY-MM' or 'YYYY-MM-DD'; pad so they sort as strings."""
    d = str(item.get("date", "0000"))
    return d + "-00-00"[len(d) - 4:] if len(d) < 10 else d


def nice_date(d, with_month=True):
    d = str(d)
    parts = d.split("-")
    if len(parts) >= 2 and with_month:
        return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}"
    return parts[0]


def year(d):
    return str(d)[:4]


def build():
    profile = load("profile")
    areas = load("areas")
    academic = load("academic")
    policy = sorted(load("policy"), key=sortkey, reverse=True)
    gov = load("government")
    media = sorted(load("media"), key=sortkey, reverse=True)
    teaching = load("teaching")
    area_by_key = {a["key"]: a for a in areas}

    published = sorted(academic["published"], key=sortkey, reverse=True)
    working = academic["working"]
    # Area pages show the same number of policy and academic items so the columns match.
    N = 5
    papers = sorted(published + working, key=sortkey, reverse=True)

    # One combined list for the Publications page, each row tagged for the filters.
    rows = []
    for p in published:
        rows.append({**p, "type": "article", "type_label": "Journal article"})
    for p in working:
        rows.append({**p, "type": "working", "type_label": "Working paper"})
    for p in policy:
        t = "policy" if p["kind"] == "research" else "commentary"
        label = {"research": "Policy research", "commentary": "Commentary", "op-ed": "Op-ed"}[p["kind"]]
        rows.append({**p, "type": t, "type_label": label})
    for t in gov["testimony"]:
        rows.append({**t, "type": "testimony", "type_label": "Testimony", "outlet": t["body"]})
    rows.sort(key=sortkey, reverse=True)

    this_year = dt.date.today().year
    recent_years = {str(this_year), str(this_year - 1)}

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    env.filters["nice_date"] = nice_date
    env.filters["year"] = year

    def bust(path):
        """Append a short content hash so browsers fetch a changed file right away instead of a cached copy."""
        f = ROOT / path
        if not f.exists():
            return path
        return f"{path}?v={hashlib.md5(f.read_bytes()).hexdigest()[:8]}"
    env.filters["bust"] = bust
    common = dict(profile=profile, areas=areas, area_by_key=area_by_key,
                  updated=f"{MONTHS[dt.date.today().month - 1]} {this_year}")

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "research").mkdir(parents=True)

    def render(template, path, **ctx):
        depth = path.count("/")
        html = env.get_template(template).render(**common, base="../" * depth, page=path, **ctx)
        (OUT / path).write_text(html, encoding="utf-8")

    render("index.html", "index.html", published=published[:3], testimony=gov["testimony"])

    render("research_index.html", "research/index.html")

    for a in areas:
        k = a["key"]
        has = lambda x: k in x.get("topics", [])
        render("area.html", f"research/{k}.html", area=a,
               policy=[p for p in policy if has(p)][:N],
               policy_total=sum(1 for p in policy if has(p)),
               academic=[p for p in papers if has(p)][:N],
               academic_total=sum(1 for p in papers if has(p)),
               working=[],
               testimony=[t for t in gov["testimony"] if has(t)],
               govitems=[i for s in gov["service"] for i in s["items"] if has(i)],
               media=[m for m in media if has(m)][:4],
               media_total=sum(1 for m in media if has(m)))

    years = []
    for r in rows:
        y = year(r["date"])
        if not years or years[-1]["year"] != y:
            years.append({"year": y, "rows": []})
        years[-1]["rows"].append(r)
    render("publications.html", "publications.html",
           recent=[y for y in years if y["year"] in recent_years],
           older=[y for y in years if y["year"] not in recent_years],
           in_progress=academic["in_progress"], total=len(rows))

    render("policy.html", "policy.html", gov=gov)

    myears = []
    for m in media:
        y = year(m["date"])
        if not myears or myears[-1]["year"] != y:
            myears.append({"year": y, "rows": []})
        myears[-1]["rows"].append(m)
    render("media.html", "media.html", featured=[m for m in media if m.get("featured")],
           recent=[y for y in myears if y["year"] in recent_years],
           older=[y for y in myears if y["year"] not in recent_years])

    render("teaching.html", "teaching.html", teaching=teaching)

    shutil.copytree(ROOT / "static", OUT / "static")
    if (ROOT / "cv.pdf").exists():
        shutil.copy(ROOT / "cv.pdf", OUT / "cv.pdf")
    if (ROOT / "CNAME").exists():
        shutil.copy(ROOT / "CNAME", OUT / "CNAME")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {sum(1 for _ in OUT.rglob('*.html'))} pages into {OUT}")


if __name__ == "__main__":
    build()
