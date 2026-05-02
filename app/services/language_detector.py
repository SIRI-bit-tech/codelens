"""Programming language detection from file extension or content"""

import re
from typing import Optional
from app.config.constants import LANGUAGE_EXTENSIONS, SUPPORTED_LANGUAGES


class LanguageDetector:
    """Detects programming language from file extension or code content"""

    @staticmethod
    def detect_from_extension(file_extension: str) -> Optional[str]:
        """Detect language from file extension"""
        return LANGUAGE_EXTENSIONS.get(file_extension.lower())

    @staticmethod
    def detect_from_content(code: str) -> str:
        """Detect language from code content using heuristics"""
        code_lower = code.lower()
        code_lines = code.split("\n")

        if "def " in code and ("import " in code or "from " in code):
            return "python"

        if "function " in code or "const " in code or "let " in code or "var " in code:
            if "=>" in code or "console.log" in code:
                return "javascript"

        if "interface " in code and ("export " in code or "import " in code):
            if ": " in code and ("string" in code_lower or "number" in code_lower):
                return "typescript"

        if "public class " in code or "private class " in code:
            if "System.out" in code or "public static void main" in code:
                return "java"

        if "#include" in code and ("int main" in code or "void main" in code):
            if "std::" in code or "cout" in code or "cin" in code:
                return "cpp"
            return "c"

        if "using System" in code or "namespace " in code:
            if "Console.WriteLine" in code or "public class" in code:
                return "csharp"

        if "func " in code and "package " in code:
            return "go"

        if "fn " in code and ("let " in code or "mut " in code):
            if "impl " in code or "trait " in code:
                return "rust"

        if "<?php" in code or "$" in code and "function" in code:
            return "php"

        if "def " in code and "end" in code:
            if "@" in code or "puts " in code or "require " in code:
                return "ruby"

        if "func " in code and ("var " in code or "let " in code):
            if "import " in code and ("UIKit" in code or "SwiftUI" in code):
                return "swift"

        if "fun " in code and ("val " in code or "var " in code):
            return "kotlin"

        if re.search(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b", code, re.IGNORECASE):
            return "sql"

        if "<html" in code_lower or "<!doctype html" in code_lower:
            return "html"

        if re.search(r"[.#]\w+\s*{", code) and ("color:" in code_lower or "background:" in code_lower):
            return "css"

        if code.strip().startswith("{") and code.strip().endswith("}"):
            try:
                import json
                json.loads(code)
                return "json"
            except:
                pass

        if re.search(r"^\w+:\s*$", code, re.MULTILINE):
            if "---" in code or re.search(r"^\s*-\s+\w+", code, re.MULTILINE):
                return "yaml"

        if code.startswith("#!") or "#!/bin/" in code:
            return "shell"

        if "<-" in code and ("library(" in code or "data.frame" in code):
            return "r"

        if "void main()" in code and "Widget " in code:
            return "dart"

        return "python"

    @staticmethod
    def detect(code: str, file_extension: Optional[str] = None) -> str:
        """
        Detect language from extension first, then content

        Returns:
            Detected language name
        """
        if file_extension:
            lang = LanguageDetector.detect_from_extension(file_extension)
            if lang:
                return lang

        return LanguageDetector.detect_from_content(code)
