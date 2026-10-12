# 徐晗洋 · Hanyang Xu

Personal academic / internship portfolio: **https://xuhanyang3.github.io/**

Buildless HTML + CSS. No framework, JavaScript, trackers, external fonts, or paid hosting. GitHub Pages publishes `main` → `/docs`.

## Local preview

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:4173`. The page also works by opening `docs/index.html` directly.

## Checks

```sh
python3 -m unittest discover -s tests -v
```

Checks cover section navigation, local visitor assets, valid PDF download and email-only contact on the HTML page. For layout changes, also check desktop and mobile widths in a browser.

## Updating content

- `docs/index.html`: biography, paper status, project, education, skills and contact.
- `docs/styles.css`: responsive layout and visual styling.
- `docs/assets/Hanyang-Xu-CV.pdf`: downloadable resume. Replace only with a version approved for public sharing.
- `docs/assets/portrait.jpg`: original portrait extracted from the supplied resume.
- `docs/sitemap.xml`: update the modification date when changing the page.

Push reviewed changes to `main` to redeploy. Keep the downloadable CV and paper statuses synchronized with the page.

## Content provenance and publication status

The initial page follows the supplied 2026-09-28 resume, with public research links checked on 2026-10-12.

- AdaPUV: first author; submitted to **npj Digital Medicine**, minor revision returned. This is **not** an acceptance or published-paper claim.
- Beyond Classification: **BMVC 2026 Accepted**, co-first author, second listed. Links point to the public [arXiv paper](https://arxiv.org/abs/2609.05937), [authors' project page](https://acenbai.github.io/projects/Beyond-Classification/), and [authors' code repository](https://github.com/AcenBai/Beyond-Classification-code).
- Knowledge fusion project: participation and contribution described as in the supplied resume. No unprovided publication status or private manuscript is exposed.

The HTML page displays only the email address. **The downloadable original resume retains its phone number, as explicitly requested by the owner.** The PDF and portrait are personal materials, not reusable website-template assets. No third-party research illustrations or project-page source code were copied.
