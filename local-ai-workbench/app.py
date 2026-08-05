"""AI Teacher Workbench - web interface.

A single-file Flask app that gives teachers:
  1. A chat box to talk to the model (local Ollama or Ollama Cloud).
  2. A prompt library of copy-paste-ready examples.
  3. A Rubric Grader that uploads student work and writes a feedback PDF
     for every student, then downloads them as a zip.

Run locally with:  python app.py
Then open http://localhost:5000 in your browser.
"""
from __future__ import annotations

import io
import json
import os
import traceback
from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from werkzeug.utils import secure_filename

from config import config
from file_reader import SUPPORTED_EXTENSIONS, EXT_LABELS
from grading import GradeJob
from llm import LLMProvider, ProviderError
from prompts import PROMPTS, PROMPT_LOOKUP

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_UPLOAD_MB * 1024 * 1024


def _provider() -> LLMProvider:
    try:
        return LLMProvider()
    except ProviderError as e:
        raise e


@app.template_filter("nl2br")
def nl2br(value):
    return str(value).replace("\n", "<br>")


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    try:
        health = _provider().health_detail()
    except ProviderError as e:
        health = {"ok": False, "message": str(e), "provider": config.PROVIDER, "model": config.effective_model}
    return render_template(
        "index.html",
        prompts=PROMPTS,
        config=config,
        health=health,
        ext_labels=EXT_LABELS,
    )


@app.route("/prompt/<prompt_id>")
def prompt_json(prompt_id: str):
    p = PROMPT_LOOKUP.get(prompt_id)
    if not p:
        return jsonify({"error": "not found"}), 404
    return jsonify(p)


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []
    if not message:
        return jsonify({"error": "Please type a message."}), 400

    llm = _provider()
    messages = [{"role": "system", "content": _chat_system_prompt()}]
    for h in history[-10:]:
        role = h.get("role")
        content = h.get("content")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": message})

    try:
        reply = llm.chat(messages)
        return jsonify({"reply": reply})
    except ProviderError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {e}"}), 500


def _chat_system_prompt() -> str:
    return (
        "You are a helpful, knowledgeable assistant for teachers. You help "
        "with lesson planning, differentiation, feedback drafting, and "
        "questions about teaching. You are warm and clear, and you never "
        "invent facts, sources, or student information. When you are unsure, "
        "you say so. You support teachers as the decision makers and never "
        "present yourself as a replacement for professional judgment. "
        "Write in plain language and keep answers well structured."
    )


# ---------------------------------------------------------------------------
# Rubric Grader
# ---------------------------------------------------------------------------
@app.route("/grade", methods=["GET", "POST"])
def grade():
    if request.method == "GET":
        return render_template(
            "grade.html",
            config=config,
            supported=", ".join(sorted(EXT_LABELS)),
        )

    rubric = (request.form.get("rubric") or "").strip()
    title = (request.form.get("title") or "").strip()
    teacher = (request.form.get("teacher") or "").strip()
    context = (request.form.get("context") or "").strip()
    temperature = _float_or(request.form.get("temperature"), 0.3)

    if not rubric:
        flash("Please paste a rubric.", "error")
        return redirect(url_for("grade"))
    if not title:
        title = "Untitled Assignment"

    files = request.files.getlist("student_files")
    usable = []
    for f in files:
        if not f or not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            flash(f"Skipped '{f.filename}': unsupported type.", "warning")
            continue
        usable.append((secure_filename(f.filename), f.read()))

    if not usable:
        flash("Please upload at least one student work file.", "error")
        return redirect(url_for("grade"))

    job = GradeJob(
        rubric_text=rubric,
        assignment_title=title,
        teacher_name=teacher or "Teacher",
        assignment_context=context,
        temperature=temperature,
    )
    for fn, data in usable:
        job.add_file(fn, data)

    log = []
    job.run(log=log.append)

    zip_path = job.bundle_zip()
    zip_name = zip_path.name if zip_path else None
    return render_template(
        "grade_result.html",
        results=job.results,
        errors=job.errors,
        log=log,
        zip_name=zip_name,
        zip_download_url=url_for("download_zip", name=zip_name) if zip_name else None,
        is_hosted=config.IS_HOSTED,
    )


@app.route("/download/<name>")
def download_zip(name: str):
    safe = secure_filename(name)
    p = config.OUTPUT_DIR / safe
    if not p.exists():
        return "File not found", 404
    return send_file(p, as_attachment=True)


# ---------------------------------------------------------------------------
# Status / health API (used by the status box)
# ---------------------------------------------------------------------------
@app.route("/api/status")
def api_status():
    try:
        health = _provider().health_detail()
    except ProviderError as e:
        health = {"ok": False, "message": str(e)}
    return jsonify(health)


def _float_or(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    print("\n  AI Teacher Workbench")
    print(f"  Provider: {config.PROVIDER}  |  Model: {config.effective_model}")
    print(f"  Open in your browser:  http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
