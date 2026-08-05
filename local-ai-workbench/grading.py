"""The rubric-grading workflow.

Given a rubric, a list of student work files, and the teacher's assignment
context, this module:
  1. Reads each student's file.
  2. Asks the model to score it against the rubric (returns JSON).
  3. Writes a PDF feedback sheet per student into the output folder.

Everything is built so a human reviews the output before it reaches students.
"""
from __future__ import annotations

import json
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import config
from file_reader import extract_text_from_bytes, UnsupportedFileError
from llm import LLMProvider, ProviderError
from pdf_feedback import build_feedback_pdf


class GradeJob:
    """One rubric-grading run. Holds state so the UI can show progress."""

    def __init__(
        self,
        *,
        rubric_text: str,
        assignment_title: str,
        teacher_name: str,
        assignment_context: str = "",
        temperature: float = 0.3,
    ) -> None:
        self.rubric_text = rubric_text
        self.assignment_title = assignment_title or "Untitled Assignment"
        self.teacher_name = teacher_name or "Teacher"
        self.assignment_context = assignment_context or ""
        self.temperature = temperature
        self.files: list[tuple[str, bytes]] = []  # (filename, bytes)
        self.llm = LLMProvider()
        self.errors: list[str] = []
        self.results: list[dict] = []  # per-student summary
        self.started_at = datetime.now()

    # -- loading ------------------------------------------------------------
    def add_file(self, filename: str, data: bytes) -> None:
        self.files.append((filename, data))

    # -- prompts ------------------------------------------------------------
    def _system_prompt(self) -> str:
        return (
            "You are an experienced classroom teacher giving constructive, "
            "fair, and specific feedback on student work. You grade strictly "
            "against the provided rubric. You never inflate scores to be kind. "
            "You write comments that are encouraging, actionable, and respect "
            "the student's dignity. "
            "Return your answer ONLY as valid JSON with this exact shape: "
            '{"scores": [{"criterion": "the rubric criterion", "level": "the '
            'level the student earned", "comment": "a short note"}], '
            '"overall_score": "a single overall score or level", '
            '"feedback": "a paragraph or two of warm, specific feedback for '
            'the student"}. '
            "Do not write any text before or after the JSON object."
        )

    def _user_prompt(self, student_name: str, student_text: str) -> str:
        parts = [f"Assignment: {self.assignment_title}"]
        if self.assignment_context:
            parts.append(f"Assignment context / instructions: {self.assignment_context}")
        parts.append(f"Student: {student_name}")
        parts.append("\nRUBRIC:\n" + self.rubric_text)
        parts.append("\nSTUDENT WORK:\n" + student_text)
        return "\n\n".join(parts)

    # -- parsing ------------------------------------------------------------
    @staticmethod
    def _parse_json(text: str) -> dict:
        """Parse JSON from model output, tolerating markdown fences."""
        cleaned = text.strip()
        # strip ```json ... ``` fences
        fence = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.S)
        if fence:
            cleaned = fence.group(1).strip()
        # fall back to the outermost {...} block
        if not cleaned.startswith("{"):
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                cleaned = cleaned[start : end + 1]
        return json.loads(cleaned)

    # -- run -----------------------------------------------------------------
    def run(self, log: callable = None) -> list[dict]:
        """Process every uploaded file and return per-student results.

        log is an optional callable(str) for progress messages.
        """
        def _log(msg: str) -> None:
            if log:
                log(msg)

        system = self._system_prompt()
        out_dir = config.OUTPUT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

        for filename, data in self.files:
            _log(f"Reading {filename} ...")
            try:
                student_text = extract_text_from_bytes(filename, data)
            except UnsupportedFileError as e:
                self.errors.append(f"{filename}: {e}")
                continue
            except Exception as e:
                self.errors.append(f"{filename}: could not be read ({e}).")
                continue

            # Derive a student name from the filename (drop extension).
            student_name = Path(filename).stem.replace("_", " ").replace("-", " ").strip()
            if not student_name:
                student_name = filename

            # Trim to context budget to avoid blowing the model window.
            if len(student_text) > config.MAX_CONTEXT_CHARS:
                student_text = student_text[: config.MAX_CONTEXT_CHARS] + "\n[truncated]"
                _log(f"  (long file, using first {config.MAX_CONTEXT_CHARS} characters)")

            _log(f"  Asking the model to grade {student_name} ...")
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": self._user_prompt(student_name, student_text)},
            ]
            try:
                raw = self.llm.chat(messages, temperature=self.temperature)
            except ProviderError as e:
                self.errors.append(f"{filename}: {e}")
                continue
            except Exception as e:
                self.errors.append(f"{filename}: model error ({e}).")
                continue

            try:
                parsed = self._parse_json(raw)
                scores = parsed.get("scores", [])
                overall = parsed.get("overall_score", "See feedback")
                feedback = parsed.get("feedback", raw)
            except (json.JSONDecodeError, ValueError):
                self.errors.append(
                    f"{filename}: the model did not return usable JSON. "
                    "Try a stronger model, or rerun."
                )
                continue

            # Write the PDF.
            safe_name = re.sub(r"[^A-Za-z0-9 _-]", "", student_name).strip() or "Student"
            out_pdf = out_dir / f"{safe_name} - feedback.pdf"
            try:
                build_feedback_pdf(
                    student_name=student_name,
                    assignment_title=self.assignment_title,
                    teacher_name=self.teacher_name,
                    scores=scores,
                    overall_score=overall,
                    feedback_markdown=feedback,
                    output_path=out_pdf,
                )
            except Exception as e:
                self.errors.append(f"{filename}: PDF write failed ({e}).")
                continue

            self.results.append(
                {
                    "student": student_name,
                    "overall": overall,
                    "pdf": str(out_pdf),
                    "feedback": feedback,
                }
            )
            _log(f"  Wrote {out_pdf.name}")

        return self.results

    # -- packaging -----------------------------------------------------------
    def bundle_zip(self) -> Optional[Path]:
        """Zip all PDFs (and any per-file errors) into one download."""
        if not self.results:
            return None
        stamp = self.started_at.strftime("%Y%m%d-%H%M%S")
        zip_path = config.OUTPUT_DIR / f"feedback-{stamp}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for r in self.results:
                p = Path(r["pdf"])
                if p.exists():
                    zf.write(p, arcname=p.name)
        return zip_path
