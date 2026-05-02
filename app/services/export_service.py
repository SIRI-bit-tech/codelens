"""Export session to PDF or Markdown"""

from typing import List, Dict, Optional
from datetime import datetime
import os


class ExportService:
    """Handles exporting sessions to various formats"""

    @staticmethod
    def export_to_markdown(
        code: str,
        language: str,
        explanation: str,
        chat_history: List[Dict],
        file_path: str,
    ) -> Optional[str]:
        """
        Export session to Markdown file

        Args:
            code: Original code
            language: Programming language
            explanation: AI explanation
            chat_history: Chat messages
            file_path: Output file path

        Returns:
            Error message if failed, None if successful
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            content = f"""# CodeLens Session Export

**Date:** {timestamp}  
**Language:** {language}

---

## Code

```{language}
{code}
```

---

## Explanation

{explanation}

---

## Chat History

"""

            if chat_history:
                for msg in chat_history:
                    role = msg.get("role", "user")
                    parts = msg.get("parts", [])
                    text = parts[0] if parts else ""

                    if role == "user":
                        content += f"**You:** {text}\n\n"
                    else:
                        content += f"**CodeLens:** {text}\n\n"
            else:
                content += "*No chat history*\n"

            content += "\n---\n\n*Exported from CodeLens*\n"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return None
        except Exception as e:
            return f"Error exporting to Markdown: {str(e)}"

    @staticmethod
    def export_to_pdf(
        code: str,
        language: str,
        explanation: str,
        chat_history: List[Dict],
        file_path: str,
    ) -> Optional[str]:
        """
        Export session to PDF file

        Args:
            code: Original code
            language: Programming language
            explanation: AI explanation
            chat_history: Chat messages
            file_path: Output file path

        Returns:
            Error message if failed, None if successful
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
            from reportlab.lib.enums import TA_LEFT

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor="darkblue",
            )

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            story.append(Paragraph("CodeLens Session Export", title_style))
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph(f"<b>Date:</b> {timestamp}", styles["Normal"]))
            story.append(Paragraph(f"<b>Language:</b> {language}", styles["Normal"]))
            story.append(Spacer(1, 0.3 * inch))

            story.append(Paragraph("Code", styles["Heading2"]))
            story.append(Spacer(1, 0.1 * inch))

            code_style = ParagraphStyle(
                "Code",
                parent=styles["Code"],
                fontSize=8,
                leftIndent=20,
            )
            story.append(Preformatted(code, code_style))
            story.append(Spacer(1, 0.3 * inch))

            story.append(Paragraph("Explanation", styles["Heading2"]))
            story.append(Spacer(1, 0.1 * inch))
            for para in explanation.split("\n\n"):
                if para.strip():
                    story.append(Paragraph(para.replace("\n", "<br/>"), styles["Normal"]))
                    story.append(Spacer(1, 0.1 * inch))

            story.append(Spacer(1, 0.3 * inch))
            story.append(Paragraph("Chat History", styles["Heading2"]))
            story.append(Spacer(1, 0.1 * inch))

            if chat_history:
                for msg in chat_history:
                    role = msg.get("role", "user")
                    parts = msg.get("parts", [])
                    text = parts[0] if parts else ""

                    if role == "user":
                        story.append(Paragraph(f"<b>You:</b> {text}", styles["Normal"]))
                    else:
                        story.append(Paragraph(f"<b>CodeLens:</b> {text}", styles["Normal"]))
                    story.append(Spacer(1, 0.1 * inch))
            else:
                story.append(Paragraph("<i>No chat history</i>", styles["Normal"]))

            doc.build(story)
            return None
        except Exception as e:
            return f"Error exporting to PDF: {str(e)}"
