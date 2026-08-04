# Project Memory, AI in Education PD Hub

This file is the project-scoped memory for the AI PD site. Everything here is specific to
this repo and does not belong in global Hermes memory. Keep it current as the project evolves.

## Identity
- **School:** Ida B. Wells High School (Portland Public Schools, pps.net)
- **Owner/contact:** aansell@pps.net
- **Audience:** All teachers, all grades & subjects. Mostly Chromebooks at school; some Mac/PC at home. Google Workspace district.
- **Assumption:** Gemini in Workspace is NOT assumed available.

## The primary deliverable
A static site (GitHub Pages) that is the year-round home base for 3 whole-school PD sessions:
1. AI for teachers' daily work
2. AI with students in the classroom (teacher-supervised)
3. Teaching students to use AI well (AI literacy)

Core principles that gate every activity:
- Never lower cognitive load
- Always increase engagement
- Consider bias, race & inclusion
- Protect privacy & equity

## Approved-software workflow (IMPORTANT)
- District IT keeps the approved-software list at **LearnPlatform**:
  `https://pps.app.learnplatform.com/new/organizations/153034/organization_tools`
- The PPS AI page (official policy language + approved staff tools):
  `https://www.pps.net/departments/office-of-teaching-learning/artificial-intelligence-in-pps`
  AI Guidebook: `.../ai-guidebook` (full guidebook URL:
  `https://ppsnet.finalsite.com/departments/office-of-teaching-learning/artificial-intelligence-in-pps/ai-guidebook`)
  Guidebook sections: Intro/Objectives · AI for Staff · AI Levels of Use for Students
  (Restrictive/Moderate/Permissive) · Responsible AI Use · Data Privacy & Security · Environmental
  Impact · AI & Academic Integrity · Approved PPS AI Tools · Guidance for Families · Resources ·
  References · Feedback.
- **Rule:** Every tool on the site must reflect its PPS approval status. The Tools page leads with
  PPS-approved staff tools; denied tools are minimized to a compact "Not approved" block (no usage how-to).
- **PPS-approved AI staff tools:** Gemini, Adobe Express, Canva, Kami, Screencastify.
  Also approved for teacher use per owner CSV: NotebookLM, Ollama, Diffit, SchoolAI.
  Under review: Claude (incl. Claude for Education), ChatGPT for teachers, Microsoft Copilot/M365.
  NOT approved: ChatGPT (consumer), MagicSchool, Brisk Teaching, Khanmigo, Curipod.
- **Verified pricing (2026-08):** Claude Free $0; Pro $17/mo annual ($200 upfront) / $20 monthly;
  Max from $100/mo (5x or 20x usage); Team $20/seat annual / $25 monthly (Premium seat $100/$125).
  Claude for Education: institutional plan for students/faculty/staff at discounted rates, academic
  research & learning mode (API credits), training & enablement. "No model training on your content by
  default" on Team/Enterprise.
- **PPS key policy language** (incorporate on the site):
  - Vision: AI as "a transformative, ethical, and human-centered tool to accelerate student achievement,
    disrupt systemic inequities, and prepare every graduate for an AI-powered future."
  - AI is governed by the Acceptable Use Policy (AUP) and Administrative Directive 8.60.041-AD.
  - Approved vs Non-Approved categories; staff can use approved AI for learning design, admin tasks,
    instructional support. Always human oversight + transparency (cite AI use).
  - Never upload student work/grades/PII into AI tools unless district authorized + DPA in place.
  - Do NOT rely on AI detection tools (unreliable, bias against non-native English speakers).
  - PPS encourages Gemini with district accounts (no training on your data).
  - Student use model: Restrictive (no AI) / Moderate (AI with citation) / Permissive (AI without citation).
- When you cannot reach the list yourself, mark status honestly and/or ask the owner to supply it.
  Live data source: `district-status.csv` in the repo root.

## Policy templates
- `downloads/policy-*.docx` (+ source `.md`), department-specific AI use policies, Google-Docs-ready.
- `downloads/classroom-agreement.docx`, student-facing "Honest Work" agreement.
- Regenerate docx from md: `python3 scripts/md_to_docx.py`
- To make them live Drive links: upload .docx → open as Google Doc → swap link on policies page.

## Tool pricing research (as of 2026-08-03, verify before publishing)
See `RESEARCH-NOTES.md` for the full verified figures (Claude, MS Copilot, Ollama, MagicSchool,
Diffit, Khanmigo, etc.). Two items still unverified (blocked pages): OpenAI consumer ChatGPT
pricing, and Canva for Education free-teacher status.

## Design
- Warm, modern aesthetic (teal + gold, Lora serif headings, Lato body, warm paper bg).
- Reference site owner liked: https://diana-brewer.github.io/digital-learning-unlocked/index.html
