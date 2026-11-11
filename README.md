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

Live (since Nov 11, 2026) at https://elenaspatel.github.io/elenaspatel-site/ from the public repo `elenaspatel/elenaspatel-site`. Every push to `main` (Elena uses GitHub Desktop) builds and deploys in about a minute. elenaspatel.com still points to the old Google Site until the Namecheap switch below; until then `noindex: true` in profile.yaml keeps the github.io address out of search engines (set it to false at the switch).

Commits in this repo use GitHub's private address (274235979+elenaspatel@users.noreply.github.com, set in the repo's git config) so Elena's personal email never appears in the public history.

### Domain (Namecheap)

elenaspatel.com is registered at Namecheap, which also runs its DNS (Namecheap BasicDNS). As of Nov 2026, `www` is a CNAME to `ghs.googlehosted.com` (the old Google Site), and the bare domain uses Namecheap's URL-redirect record (192.64.119.7) to send visitors to `www`. To switch to GitHub Pages, in Namecheap → Domain List → Manage → Advanced DNS:

1. Replace the `www` CNAME with `elenaspatel.github.io`.
2. Replace the `@` URL-redirect record with four A records: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.
3. Add a `CNAME` file containing `www.elenaspatel.com` (or `elenaspatel.com`) to the repo root; build.py copies it into the site.
4. In the repo's Settings → Pages, enter the custom domain, then tick "Enforce HTTPS" once the certificate is issued. Verifying the domain under GitHub account settings → Pages guards against takeover.

Keep the Google Site untouched until the new site loads at the domain, so nothing goes dark.

## Open items

- Headshot: add `static/headshot.jpg` and set `headshot:` in profile.yaml.
- Contact lines in profile.yaml are placeholders.
- Area intros and the home headline are drafts for Elena to edit; Social insurance and Governance have no key findings yet.
