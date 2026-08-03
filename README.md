# AI in Education — Professional Learning Hub

A year-round professional learning resource for whole-school AI training, built as a static
site that lives on GitHub Pages.

## What this is

Three 40-minute PD sessions plus a year-round resource hub for using AI effectively, ethically,
and equitably in K-12 schools:

- **Session 1 — AI for Your Daily Work** (planning, differentiation, rubrics, feedback, communication)
- **Session 2 — AI With Students in the Classroom** (teacher-supervised activities, cognitive load)
- **Session 3 — Teaching Students to Use AI Well** (AI literacy, ethics, bias, academic honesty)

Plus:
- **AI Toolbox** — side-by-side tool comparisons (Gemini, Claude, ChatGPT, Ollama, education tools)
- **Free vs Paid Plans** — where student work can and can't go
- **Policies & Templates** — downloadable, department-specific AI use policies
- **Department Activities** — a year-long collaborative calendar
- **Privacy & Student Data** — FERPA-friendly plain-language rules
- **Private Chatbot (optional)** — plan for an API-driven, no-training school chatbot

## How to run it

This is a plain static site — no build step, no dependencies. Open `index.html` in a browser,
or serve it:

```bash
# any static server works, e.g. Python:
python3 -m http.server 8000
# then visit http://localhost:8000
```

## How to deploy to GitHub Pages

1. Create a repo on GitHub, e.g. `yourname/ai-pd-2026-27`.
2. Push this folder to the repo.
3. In the repo → **Settings → Pages** → under "Branch," choose `main` and the `/ (root)` folder → Save.
4. Your site will be live at `https://yourname.github.io/ai-pd-2026-27/`.

That's it — it's static HTML/CSS/JS with no external dependencies, so it works on any device,
including school Chromebooks.

## Customize for your school

- Replace `[School Name]` and `you@school.edu` in the footer and email links across all pages.
- Review `pages/tools.html` and `pages/plans.html` — tool pricing/features change; re-verify on
  official sites and update. Keep the notes in `RESEARCH-NOTES.md` current.
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
│   └── chatbot-repo.html         # Optional private chatbot
├── downloads/                    # Editable policy templates (.md)
│   ├── policy-*.md               # Per-department policies
│   └── classroom-agreement.md
└── RESEARCH-NOTES.md             # Maintainer's verified research
```

## License

Use freely for your school. No affiliation with any tool vendor.
