# Project Memory — AI in Education PD Hub

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
- This URL redirects to **ClassLink SSO** and requires district authentication
  (owner can log in if needed).
- **Rule:** Every tool recommended on the site must be checked against this approved list.
  The site's Tools and Plans pages have an "Approval status" / district column for exactly this.
- When you cannot reach the list yourself, mark status as "Unverified — check district list"
  and/or ask the owner to pull it.

## Policy templates
- `downloads/policy-*.docx` (+ source `.md`) — department-specific AI use policies, Google-Docs-ready.
- `downloads/classroom-agreement.docx` — student-facing "Honest Work" agreement.
- Regenerate docx from md: `python3 scripts/md_to_docx.py`
- To make them live Drive links: upload .docx → open as Google Doc → swap link on policies page.

## Tool pricing research (as of 2026-08-03, verify before publishing)
See `RESEARCH-NOTES.md` for the full verified figures (Claude, MS Copilot, Ollama, MagicSchool,
Diffit, Khanmigo, etc.). Two items still unverified (blocked pages): OpenAI consumer ChatGPT
pricing, and Canva for Education free-teacher status.

## Design
- Warm, modern aesthetic (teal + gold, Lora serif headings, Lato body, warm paper bg).
- Reference site owner liked: https://diana-brewer.github.io/digital-learning-unlocked/index.html
