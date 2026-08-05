"""Generate a clean, printable PDF of AI feedback for one student.

Uses ReportLab, which is pure Python and works on every OS. The PDF has a
friendly header, the rubric result table, and the model's feedback text.

Important: this tool drafts feedback. A human must read, edit, and approve
before anything is given to a student.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config import config

HEADER_BG = colors.HexColor("#0b5e54")  # teal, matches the site palette
ACCENT = colors.HexColor("#b8860b")     # gold accent


def _safe(text: str) -> str:
    """Escape XML-ish characters so Paragraph doesn't choke."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_feedback_pdf(
    *,
    student_name: str,
    assignment_title: str,
    teacher_name: str,
    scores: list[dict],
    overall_score: str,
    feedback_markdown: str,
    output_path: Path,
) -> Path:
    """Write a PDF to output_path and return it.

    scores: list of {"criterion": str, "level": str, "comment": str}
    feedback_markdown: plain text (markdown-ish) the model wrote.
    """
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="H1",
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=HEADER_BG,
            spaceBefore=12,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#555555"),
        )
    )

    story = []

    # Header band
    header_table = Table(
        [[Paragraph(f"<b>{_safe(assignment_title)}</b>", styles["H1"])],
         [Paragraph(_safe(f"Student: {student_name}"), styles["Body"])],
         [Paragraph(_safe(f"Teacher: {teacher_name}"), styles["Small"])]],
        colWidths=[6.5 * inch],
    )
    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HEADER_BG),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 12))

    # Rubric table
    if scores:
        story.append(Paragraph("Rubric Results", styles["H2"]))
        rows = [
            [
                Paragraph("<b>Criterion</b>", styles["Body"]),
                Paragraph("<b>Level</b>", styles["Body"]),
                Paragraph("<b>Teacher note</b>", styles["Body"]),
            ]
        ]
        for s in scores:
            rows.append(
                [
                    Paragraph(_safe(s.get("criterion", "")), styles["Body"]),
                    Paragraph(_safe(s.get("level", "")), styles["Body"]),
                    Paragraph(_safe(s.get("comment", "")), styles["Body"]),
                ]
            )
        rubric = Table(rows, colWidths=[1.7 * inch, 1.1 * inch, 3.7 * inch])
        rubric.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(rubric)
        story.append(Spacer(1, 10))

    story.append(
        Paragraph(f"Overall score: <b>{_safe(overall_score)}</b>", styles["H2"])
    )

    story.append(Paragraph("Detailed Feedback", styles["H2"]))
    for para in str(feedback_markdown).split("\n\n"):
        clean = para.strip()
        if not clean:
            continue
        story.append(Paragraph(_safe(clean), styles["Body"]))

    story.append(Spacer(1, 16))
    story.append(
        Paragraph(
            "<i>This feedback was drafted with AI assistance. It must be "
            "reviewed, edited, and approved by a teacher before being shared "
            "with a student.</i>",
            styles["Small"],
        )
    )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=f"AI Feedback - {student_name}",
    )
    doc.build(story)
    return output_path
