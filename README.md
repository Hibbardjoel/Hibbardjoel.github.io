# Joel Hibbard — resume site

A data-driven resume. One master file holds every verified fact, and tailored variants are generated per job description.

```
data/master.json          single source of truth (bullets carry ids, tags, weights)
tailored/<slug>.json      job-specific variants (same schema)
index.html                renders master or a variant: /?v=<slug>
tools/score_jd.py         ranks master bullets against a JD + lists evidence gaps
build.py                  inlines master.json into index.html (offline / single-file copy)
linkedin.md               LinkedIn copy aligned to the master
```

## Publish on GitHub Pages

1. Create a public repo named **`Hibbardjoel.github.io`**. That name serves the site at `https://hibbardjoel.github.io`.
2. Push these files to `main`.
3. In the repo, go to Settings → Pages → Source and choose "Deploy from a branch", with `main` and `/ (root)`.
4. Each tailored version lives at `https://hibbardjoel.github.io/?v=<slug>`. The sample is `?v=sample-director-enterprise-apps`.

```bash
git init && git add . && git commit -m "Resume site"
git branch -M main
git remote add origin https://github.com/Hibbardjoel/Hibbardjoel.github.io.git
git push -u origin main
```

After editing `data/master.json`, run `python3 build.py` so the inline fallback stays in sync.

## Tailoring for a job

Use the **tailor-resume** skill in Claude and paste the JD. It runs `tools/score_jd.py`, rewrites a variant without inventing anything, and writes `tailored/<slug>.json`. It also gives you ATS text and a gap report.

The "Save as PDF" button prints a two-page version. It leaves out the skill-bridge, capability and earlier-career sections and shows only the first 4 bullets per role, so put the strongest bullets first in each variant.

## Privacy note

Tailored files are public once pushed. If you'd rather not reveal which companies you're applying to, give slugs neutral names (for example `director-ent-apps-a`), or keep tailored files in a private branch and export the PDFs.
