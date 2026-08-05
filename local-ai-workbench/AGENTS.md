# Instructions for AI assistants working in this repository

This file tells AI coding assistants how to work safely and correctly inside
this repo. Read it before making any change.

## What this repo is

A local-first web app for K-12 teachers. It provides a private chat assistant
and a Rubric Grader that reads student work files and produces a feedback PDF
per student. It runs on the teacher's own machine (or their own Ollama Cloud
account). It must work on Windows, macOS, and Linux with minimal setup.

## Hard rules

1. **All configuration lives in `.env` (or environment variables).** Never
   hard-code an API key, base URL, model name, or path in a `.py` file. The
   source of truth for settings is `config.py`, which reads `config.Config`
   from the environment and loads `.env` if present.
2. **Never commit secrets.** `.env` is git-ignored. Never paste a real API key
   into code, tests, docs, or a commit message. Use the `.env.example` template
   for any new variable.
3. **Do not break cross-platform support.** The app targets Windows, macOS,
   and Linux. Avoid OS-specific code paths unless they are guarded and
   documented. Prefer the standard library or the dependencies already listed
   in `requirements.txt`.
4. **No em dashes (—) in any user-facing text.** The project owner considers
   the em dash a giveaway of AI writing. Use periods or commas instead. This
   applies to UI copy, prompts in `prompts.py`, docs, and the site page.
5. **Human oversight is a feature, not a caveat.** The Rubric Grader drafts
   feedback. The PDFs and UI must always remind the teacher to review before
   sharing. Never remove the human-review language.
6. **Graceful failures.** File reading and model calls must fail with a clear,
   friendly message, never a crash. Each student file is processed
   independently; one bad file must not stop the rest.

## Architecture

- `app.py` - Flask web app (routes, chat API, rubric grader view).
- `config.py` - loads `.env` / env vars, exposes `config.Config`.
- `llm.py` - `LLMProvider` talks to local Ollama or Ollama Cloud
  (both OpenAI-compatible `/chat/completions`).
- `file_reader.py` - text extraction from PDF, DOCX, TXT, MD, CSV.
- `grading.py` - `GradeJob` runs the rubric workflow and writes PDFs.
- `pdf_feedback.py` - builds each feedback PDF with ReportLab.
- `prompts.py` - the copy-paste example prompt library.
- `templates/` - Jinja2 HTML.
- `static/` - CSS and JS.
- `setup.sh` / `run.sh` - macOS/Linux. `setup.bat` / `run.bat` - Windows.
- `requirements.txt` - Python dependencies.

## Adding a new example prompt

Add it to the `PROMPTS` list in `prompts.py` as a dict with keys:
`id`, `title`, `tag`, `uses_upload` (bool), `hint` (optional), and `text`.
The `text` is a self-contained system prompt with `[BRACKETS]` placeholders.
It must always keep the teacher as the decision maker and forbid inventing
facts. No em dashes.

## Running / testing locally

```
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./run.sh            # then open http://localhost:5000
```

Tests are lightweight. After editing a module, import it to catch syntax
errors:
```
./.venv/bin/python -c "import app, grading, llm, file_reader, pdf_feedback, prompts, config"
```

## Hosted (Vercel) mode

`vercel.json`, `api/index.py`, and `config.py`'s `IS_HOSTED` flag let the same
app run on Vercel's serverless platform for a live demo. On Vercel the `.env`
becomes Vercel environment variables, and disk is ephemeral (uploads/PDFs live
only for the life of a request). Keep the two modes in sync: any config change
must work in both. Never add a dependency to `requirements.txt` that Vercel
cannot install (keep it pure Python with wheels).

## Do not

- Rename or refactor working modules without a reason.
- Add drive-by formatting.
- Commit, push, or rewrite git history unless asked.
- Read or print `output/`, `uploads/`, or `.env` contents.
