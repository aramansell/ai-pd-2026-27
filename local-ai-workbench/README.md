# AI Teacher Workbench

A private, local-first AI workspace for teachers. Run it on your own computer
for free with **Ollama**, or connect your **Ollama Cloud** account. All
configuration lives in one `.env` file. Works on **Windows, macOS, and Linux**.

This is part of the "AI in Education" professional learning hub. It is
designed so a teacher with minimal technical know-how can get it running in
about 15 minutes.

## What you can do

- **Chat** with a private AI assistant for lesson planning, feedback,
  differentiation, assessment, and more.
- **Prompt library** of copy-paste example prompts, each with `[BRACKETS]`
  to fill in.
- **Rubric Grader**: paste a rubric, upload a folder of student work, and get
  a feedback PDF for every student, packed into one download.

## The one rule

AI drafts. A human teacher reviews, edits, and approves everything before it
reaches a student. Never upload more student information than the assignment
requires.

## Quick start

1. Choose your AI engine:
   - **Local (free, offline):** install Ollama at https://ollama.com/download,
     then `ollama pull llama3.2`.
   - **Cloud:** create a free key at https://ollama.com/signup.
2. Install Python 3.9+ from https://www.python.org/downloads/ (Windows: tick
   "Add Python to PATH").
3. Download this repo (Code > Download ZIP) and unzip it.
4. Run setup, then start:
   - **Windows:** double-click `setup.bat`, then `run.bat`.
   - **macOS/Linux:** in Terminal run `./setup.sh`, then `./run.sh`.
5. Open **http://localhost:5000**.

Full instructions for every step, including per-OS notes and troubleshooting,
are in **[SETUP.md](SETUP.md)**.

## Configuration

Copy `.env.example` to `.env` and edit it. That is the whole config. To switch
to Ollama Cloud, set `PROVIDER=cloud` and add your `OLLAMA_API_KEY`.

| Variable | Purpose | Default |
|---|---|---|
| `PROVIDER` | `ollama` (local) or `cloud` | `ollama` |
| `OLLAMA_BASE_URL` | Local Ollama address | `http://localhost:11434` |
| `OLLAMA_MODEL` | Local model name | `llama3.2` |
| `CLOUD_BASE_URL` | Cloud API base | `https://api.ollama.com/v1` |
| `CLOUD_MODEL` | Cloud model | `llama3.3` |
| `OLLAMA_API_KEY` | Cloud API key (leave blank for local) | (empty) |
| `MAX_UPLOAD_MB` | Largest allowed file | `25` |
| `MAX_STUDENT_WORK_FILES` | Max files per grade run | `60` |
| `MAX_CONTEXT_CHARS` | Max characters sent to the model per file | `40000` |
| `REQUEST_TIMEOUT_S` | Model request timeout | `600` |
| `SECRET_KEY` | Session secret, change it | random-ish |

## Project layout

```
app.py            Flask web app
config.py         .env / environment configuration
llm.py            talks to local Ollama or Ollama Cloud
file_reader.py    reads PDF, DOCX, TXT, MD, CSV
grading.py        rubric grading workflow
pdf_feedback.py   builds feedback PDFs
prompts.py        example prompt library
templates/        web pages
static/           CSS and JS
setup.sh/run.sh   macOS + Linux
setup.bat/run.bat Windows
SETUP.md          full setup guide
AGENTS.md         instructions for AI assistants
```

## Hosting a live demo (optional)

`vercel.json`, `api/index.py`, and the `IS_HOSTED` flag let the same app run
on Vercel's free tier for a public demo that visitors can try without
downloading. See `vercel.json` and [SETUP.md](SETUP.md#hosting-a-live-demo)
for how. On hosted mode the `.env` values become Vercel environment variables
and disk is ephemeral.

## License / status

Built for professional development. Tool pricing and API details change
often; verify on the provider's official site before relying on it. Not
affiliated with any tool vendor. Feedback, drafting, and the human-review
rule are the point: this is a helper, not a replacement for a teacher.
