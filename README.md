# AI in Education, Professional Learning Hub

A year-round professional learning resource for whole-school AI training, built as a static
site that lives on GitHub Pages.

## What this is

Three 40-minute PD sessions plus a year-round resource hub for using AI effectively, ethically,
and equitably in K-12 schools:

- **Session 1, AI for Your Daily Work** (planning, differentiation, rubrics, feedback, communication)
- **Session 2, AI With Students in the Classroom** (teacher-supervised activities, cognitive load)
- **Session 3, Teaching Students to Use AI Well** (AI literacy, ethics, bias, academic honesty)

Plus:
- **AI Toolbox**, PPS-approved AI tools for staff, plus tools under review and a compact not-approved list
- **Free vs Paid Plans**, where student work can and can't go
- **Policies & Templates**, downloadable, department-specific AI use policies
- **Department Activities**, a year-long collaborative calendar
- **Privacy & Student Data**, FERPA-friendly plain-language rules
- **AI Teacher Workbench (optional)**, a free hosted AI workspace teachers use right in the browser, with their own Ollama Cloud key

## How to run it

The source is plain static HTML/CSS/JS with no dependencies, so you can open `index.html` in a
browser or serve it directly. There is an optional build step for deployment (see below), but it
is not needed for local work:


```bash
# any static server works, e.g. Python:
python3 -m http.server 8000
# then visit http://localhost:8000
```

## How to deploy to GitHub Pages (GitHub Actions)

This repo includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that builds the
site into `dist/` and deploys it to GitHub Pages automatically on every push to `main`.

1. Create a repo on GitHub, e.g. `yourname/ai-pd-2026-27`, and push this folder to it.
2. In the repo → **Settings → Pages**, under "Build and deployment", set **Source** to
   **GitHub Actions**.
3. Push to `main` (or run the workflow manually from the Actions tab).
4. Your site will be live at `https://yourname.github.io/ai-pd-2026-27/`.

### Building locally (optional)

The build is a plain Node script with no third-party dependencies:

```bash
npm install     # once, to generate the lock file
npm run build   # writes the deployable site into dist/
npm run dev     # rebuild automatically on save (watch mode)
```

The site itself is static HTML/CSS/JS with no external dependencies (fonts are self-hosted), so
it works on any device, including school Chromebooks. The build keeps the shared header/footer
and the Tools/Plans tables in sync from single sources (see Structure below).

## Customize for your school

- Replace `Ida B. Wells High School` and `aansell@pps.net` in the footer and email links across all pages.
- Update the Tools and Plans tables in `src/data/tools.json` (the single source), then run
  `npm run build`. Tool pricing/features change; re-verify on official sites. Keep the notes in
  `RESEARCH-NOTES.md` current.
- Edit the shared site header/footer in `src/_includes/` and rebuild; every page gets the change.
- Make the department policy templates in `downloads/` your own.

## Structure

```
ai-pd-2026-27/
├── index.html                    # Home hub
├── assets/
│   ├── css/style.css             # Design system
│   └── js/main.js                # Nav, accordion, tabs
├── pages/
│   ├── pd-overview.html
│   ├── pd1-teachers-tools.html
│   ├── pd2-classroom.html
│   ├── pd3-teaching-ai.html
│   ├── tools.html                # Tool comparisons
│   ├── plans.html                # Free vs paid vs workspace
│   ├── policies.html             # Policy template index
│   ├── department-activities.html
│   ├── privacy.html
│   ├── resources.html            # Frameworks, deep dives
│   └── chatbot-repo.html         # Hosted AI Teacher Workbench (bring your own key)
├── downloads/                    # Editable policy templates (.docx, Google-Docs-ready)
│   ├── policy-*.docx             # Per-department policies
│   └── classroom-agreement.docx
├── scripts/
│   └── md_to_docx.py             # Rebuilds the .docx templates from the .md sources
├── src/
│   ├── _includes/
│   │   ├── header.html           # Shared header + nav (single source, injected by build)
│   │   └── footer.html           # Shared footer (single source, injected by build)
│   └── data/
│       └── tools.json            # Data behind the Tools & Plans tables
├── .github/
│   └── workflows/deploy.yml      # GitHub Actions: build + deploy to Pages
├── build.js                      # Build: injects shared header/footer + tables → dist/
├── package.json                  # npm scripts: build / dev
├── dist/                         # Generated deployable site (built, git-ignored)
└── RESEARCH-NOTES.md             # Maintainer's verified research
```

### Updating the policy templates

The source of truth is the `.md` files that live alongside each `.docx` in `downloads/` (kept so
content is easy to edit). To regenerate the Word files after editing the markdown:

```bash
python3 -m pip install python-docx   # once
python3 scripts/md_to_docx.py
```

The `.docx` templates are designed to be **uploaded to Google Drive** (they open as Google Docs on
Chromebooks). To make them live links: upload each `.docx` to Drive → open as Google Docs → set
sharing → replace the link on the [Policies page](pages/policies.html) with the Drive share URL.

## License

Use freely for your school. No affiliation with any tool vendor.
