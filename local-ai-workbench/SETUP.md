# AI Teacher Workbench - Setup Guide

This guide walks you through setting up your own private, local AI workspace
for teachers. It works on **Windows, macOS, and Linux**. Every setting lives in
a single `.env` file, so you control exactly where your data goes.

**What you get:**
- A private chat assistant for planning, feedback, differentiation, and more.
- A library of copy-paste example prompts.
- A **Rubric Grader** that reads student work and writes a feedback PDF for
  every student, packaged into one download.
- A choice of AI engine: **free and fully offline** (local Ollama), or
  **Ollama Cloud** (works without installing a model, free tier available).

**The single most important rule:** AI drafts feedback. A human teacher reads,
edits, and approves everything before it reaches a student. Never upload more
student information than the assignment requires, and never rely on AI
judgment as the grade of record.

---

## Table of contents

1. [Before you start](#1-before-you-start)
2. [Choose your AI engine](#2-choose-your-ai-engine)
3. [Install Python](#3-install-python)
4. [Get the files](#4-get-the-files)
5. [One-time setup](#5-one-time-setup)
6. [Configure .env](#6-configure-env)
7. [Start the app](#7-start-the-app)
8. [Use the Rubric Grader](#8-use-the-rubric-grader)
9. [Troubleshooting](#9-troubleshooting)
10. [Privacy and safety](#10-privacy-and-safety)

---

## 1. Before you start

You need about 15 minutes and the ability to run a couple of commands. No
programming experience required. Everything here is copy-paste ready.

You have two choices for the AI engine, and you can switch later by editing
one line in `.env`:

| | **Local Ollama** | **Ollama Cloud** |
|---|---|---|
| Cost | Free | Free tier, or small paid tiers |
| Works offline | Yes | No, needs internet |
| Install software | Yes (Ollama app) | No |
| Privacy | Strongest, nothing leaves your device | Data goes to Ollama's cloud API (not used to train) |
| Setup effort | Slightly more | Less |

**Recommendation for most teachers:** start with **Ollama Cloud** (no model
download, just works). If you want the strongest privacy or you are offline,
use **local Ollama**.

---

## 2. Choose your AI engine

### Option A: Local Ollama (free, offline)

1. Go to **https://ollama.com/download** and install the app for your system.
2. After installing, open a terminal and pull a small model:
   - **Windows:** open Command Prompt (`Win+R`, type `cmd`, Enter).
   - **macOS/Linux:** open Terminal.
   - Then run:
     ```
     ollama pull llama3.2
     ```
3. Leave the Ollama app running (it runs in the background). On first use it
   may need to download the model once.

The default model in `.env` is `llama3.2`, which is fast and works on most
computers. Other good choices: `qwen2.5`, `gemma2`, `llama3.1`. If you have a
powerful computer you can try `llama3.3` or `mistral`.

### Option B: Ollama Cloud API

1. Go to **https://ollama.com/signup** and create a free account.
2. In your account dashboard, create an **API key**.
3. Copy that key. You will paste it into `.env` in step 6.

Ollama Cloud offers a free tier. If you go past it, you set your own budget in
your dashboard, and the app never spends anything without your `.env` pointing
at it.

---

## 3. Install Python

The app is written in Python. It needs Python 3.9 or newer.

- **Windows:** download from **https://www.python.org/downloads/**. During
  install, **tick the box "Add Python to PATH"**. This is essential.
- **macOS:** download from **https://www.python.org/downloads/** and run the
  installer.
- **Linux (Ubuntu/Debian):**
  ```
  sudo apt update && sudo apt install python3 python3-venv python3-pip
  ```

---

## 4. Get the files

You can either clone the repository or download it as a zip.

**Clone with git (if you use git):**
```
git clone <YOUR_REPO_URL> ai-workbench
cd ai-workbench
```

**Or download as a zip:** go to the repository page on GitHub, click the green
**Code** button, choose **Download ZIP**, extract it, and open the extracted
folder in your terminal.

From here on, the instructions assume you are inside the `ai-workbench`
folder.

---

## 5. One-time setup

### Windows
Double-click **`setup.bat`**, or open Command Prompt in the folder and run:
```
setup.bat
```

### macOS / Linux
Open Terminal in the folder and run:
```
chmod +x setup.sh run.sh
./setup.sh
```

The setup script creates a private Python environment (`.venv`), installs the
few libraries it needs, and copies `.env.example` to `.env` for you.

---

## 6. Configure `.env`

Open the `.env` file in any text editor (Notepad, TextEdit, or VS Code). It
looks like a simple list of `NAME=value` lines.

- To use **local Ollama**, make sure the first line reads `PROVIDER=ollama`.
- To use **Ollama Cloud**, change it to `PROVIDER=cloud`, then paste your API
  key after the `OLLAMA_API_KEY=` line (no quotes, no spaces around the `=`):
  ```
  PROVIDER=cloud
  OLLAMA_API_KEY=paste-your-key-here
  ```

Save the file. That is the entire configuration.

> Security note: `.env` is listed in `.gitignore`, so your key is never
> committed to git. Never rename `.env` to something else, and never paste
> your key into a chat, an email, or a shared file.

---

## 7. Start the app

### Windows
Double-click **`run.bat`**, or:
```
run.bat
```

### macOS / Linux
```
./run.sh
```

You will see a message like:
```
Open in your browser:  http://localhost:5000
```

Open that address in your browser. You should see the workbench with a status
box at the top telling you whether your AI engine is ready.

If the status box shows "Not ready", read the message. The two most common
causes are:
- **Local Ollama:** Ollama is not running, or the model has not been pulled
  (run `ollama pull llama3.2`).
- **Cloud:** the API key is missing or wrong in `.env`.

To stop the app later, close the terminal window or press `Ctrl+C`.

---

## 8. Use the Rubric Grader

1. Go to the **Rubric Grader** tab.
2. Type an assignment title and your name (optional).
3. **Paste your rubric.** A rubric with criteria and performance levels works
   best, for example:
   ```
   Criterion 1: Thesis
     Exceeding: A clear, arguable, and insightful thesis.
     Meeting: A clear thesis that is arguable.
     Approaching: A thesis that is present but vague or not arguable.
     Not yet: No discernible thesis.
   Criterion 2: Evidence
     ... (and so on)
   ```
4. Add assignment context (optional) so the AI grades fairly.
5. **Upload one file per student.** Name each file with the student's name,
   e.g. `jamie-smith.docx`. Supported: PDF, Word (.docx), plain text (.txt),
   Markdown (.md), CSV (.csv).
6. Pick a strictness (temperature). Lower is more literal to the rubric.
7. Click **Generate feedback PDFs**.

The app reads each file, scores it against the rubric, and writes a
**feedback PDF per student** into the `output` folder, then offers them as one
download.

**Always review every PDF** before giving it to a student. Edit anything you
disagree with. The AI is a drafting assistant, not the grader of record.

---

## 9. Troubleshooting

**"Ollama does not appear to be running."**
The Ollama app must be running. On macOS look for the llama icon in the menu
bar; on Windows look for it in the system tray. Or run `ollama serve` in a
terminal.

**"Model X is not pulled."**
Run: `ollama pull X`, replacing X with the model name in your `.env`.

**"The model took too long to reply."**
Your computer or model is slow. In `.env`, switch to a smaller model (try
`llama3.2` or `qwen2.5`), or raise `REQUEST_TIMEOUT_S`.

**"HTTP 404 / 400 from the model API."**
Usually a wrong model name. For local Ollama, confirm the name with
`ollama list`. For cloud, check the model name at the top of your dashboard.

**Port 5000 is already in use.**
Set a different port before starting:
- Windows: `set PORT=5001` then `run.bat`
- macOS/Linux: `PORT=5001 ./run.sh`
Then open `http://localhost:5001`.

**A PDF says it has no readable text.**
That PDF is a scanned image. AI cannot read pictures of text. Export the
document as text or use a Word/text version instead.

**Nothing happens and no error shows.**
Make sure you are running the app from inside the folder where `.env` lives.

---

## 10. Privacy and safety

- **Local Ollama** keeps everything on your device. Nothing leaves the
  machine. This is the strongest privacy option.
- **Ollama Cloud** sends your prompts to Ollama's API. Ollama does not train
  on API data, but content leaves your device, so keep it to lesson content,
  not unnecessary student PII.
- **Never** paste real student names, grades, medical info, or other
  personally identifying information beyond what the assignment itself needs.
- The district's AI policy still applies. Confirm any tool against your
  school or district approved-software list before use.
- AI can be biased and can be wrong. Every output you give a student or
  family must be reviewed by you. You are responsible for the final feedback.

---

## 11. Hosting a live demo (optional)

You can put a public demo of the workbench online so visitors can try it
without downloading or installing anything. The recommended free option is
**Vercel**. This does not replace running it locally, it is an extra.

Steps:
1. Push this repo to GitHub.
2. Go to https://vercel.com and sign in with GitHub.
3. Click **Add New > Project**, import this repo (Framework: **Other**).
4. In the **Environment Variables** section, add:
   - `PROVIDER` = `cloud`
   - `OLLAMA_API_KEY` = your Ollama Cloud API key
   - `CLOUD_MODEL` = `llama3.3` (or another Ollama Cloud model)
   - `IS_HOSTED` = `true`
5. Click **Deploy**. Vercel reads `vercel.json` and routes to `api/index.py`.
6. You get a free URL like `your-app.vercel.app`.

Notes on the hosted demo:
- Local Ollama is not reachable from a server, so the demo must use
  **Ollama Cloud** (free tier or paid).
- Your API key lives only in Vercel's environment variables, never in the
  repo or the browser.
- Serverless disk is ephemeral: uploads and generated PDFs exist only for the
  life of one request. The demo shows the drafted feedback on screen instead
  of saving PDFs. The downloaded local version exports PDFs for every student.

## Command reference

| Task | Windows | macOS / Linux |
|---|---|---|
| One-time setup | `setup.bat` | `./setup.sh` |
| Start the app | `run.bat` | `./run.sh` |
| Pull a local model | `ollama pull llama3.2` | `ollama pull llama3.2` |
| List local models | `ollama list` | `ollama list` |
| Install Python | python.org | python.org / apt |

Need help? Ask a colleague who is comfortable with the command line, or a
technical staff member. This tool is optional. If it is not for you, the free
web tools on the PD hub are plenty.
