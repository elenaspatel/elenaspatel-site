# elenaspatel.com — site source

Static site for Elena Spatoulas Patel, replacing the old Google Sites page. Built by `build.py` (Python + Jinja2) from YAML data, published to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.

## How updates work

Content lives in `data/*.yaml`. Templates and styles rarely change.

| File | What it holds |
|---|---|
| `data/profile.yaml` | Bio, headline, links, contact lines, positions, education |
| `data/areas.yaml` | The five research areas (order, intro, key findings) |
| `data/academic.yaml` | Journal articles, working papers, works in progress |
| `data/policy.yaml` | Brookings/TPC/Hamilton pieces and outside op-eds |
| `data/government.yaml` | Testimony, CEA/Treasury/PRC work, advisory roles |
| `data/media.yaml` | Press, interviews, podcasts (`featured: true` = Selected list) |
| `data/teaching.yaml` | Courses and doctoral students |
| `cv.pdf` | Copy of `OneDrive/HR/CV/source/main.pdf`; refresh it whenever the CV changes |

Every item carries `topics: [...]` using the area keys `tax`, `social`, `housing`, `governance`, `postal` (primary first). That tag is what puts an item on a research-area page and in the Publications/Media filters.

Dates are `YYYY-MM-DD`, `YYYY-MM`, or `YYYY`. Lists sort newest first automatically.

## Rules (decided with Elena, Nov 2026)

- Audience is mostly policymakers and Hill staff, but the site must read as academic. Polished, not gimmicky. No news feed.
- Must work well on phones. Check any layout change at phone width (375 px), with no sideways scroll.
- White background, serif headings (Source Serif 4), sans body (Source Sans 3), TPC navy #053769.
- Research-area pages: policy research and academic research side by side, five items each by default (equal lengths), then a row with testimony, government work, and press. Pages stay short: intro, key findings, the few most recent items, then "All …" links into the filtered Publications/Media pages. Full lists live once, on those pages, with older years folded.
- Research areas, in order: Tax policy; Social insurance, health, and work; Housing and infrastructure; Governance of firms and nonprofits; Postal policy.
- Group roundups (Around the Halls, Please Discuss, expert panels) stay off the site, same as the CV.
- Key findings must come from Elena's published work. No invented numbers.
- NTJ title is "Editor".

## Build and preview locally

```bash
python3 build.py
python3 -m http.server 8000 -d _site
```

Then open http://localhost:8000. `_site/` is generated and not committed.

## Publishing

The GitHub repo (`elenaspatel/elenaspatel-site`) is **private and not published yet** (Nov 2026: Elena is still workshopping it). The deploy workflow is manual-only until then. To go live: make the repo public (free GitHub Pages needs a public repo) or use a paid plan, turn on Pages with source "GitHub Actions", and restore the `push` trigger in `.github/workflows/deploy.yml`. After that, every push to `main` (Elena uses GitHub Desktop) builds and deploys in about a minute. The custom domain is set by adding a `CNAME` file containing `elenaspatel.com` (build.py copies it) and pointing the domain's DNS at GitHub Pages.

## Open items

- Headshot: add `static/headshot.jpg` and set `headshot:` in profile.yaml.
- Contact lines in profile.yaml are placeholders.
- Area intros and the home headline are drafts for Elena to edit; Social insurance and Governance have no key findings yet.
