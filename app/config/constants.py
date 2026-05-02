"""Application-wide constants"""

APP_NAME = "CodeLens"
APP_VERSION = "1.1.0"
APP_AUTHOR = "CodeLens Team"
APP_DESCRIPTION = "AI-Powered Code Explainer for Developers"

# AI Provider Configuration
AI_PROVIDERS = ["gemini", "openai", "claude"]
AI_PROVIDER_DISPLAY_NAMES = {
    "gemini": "Google Gemini",
    "openai": "OpenAI",
    "claude": "Anthropic Claude"
}

# Gemini Configuration
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_TEMPERATURE = 0.3
GEMINI_MAX_OUTPUT_TOKENS = 8192

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.3
OPENAI_MAX_OUTPUT_TOKENS = 8192

# Claude Configuration
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
CLAUDE_TEMPERATURE = 0.3
CLAUDE_MAX_OUTPUT_TOKENS = 8192

MAX_CODE_SIZE_BYTES = 50 * 1024

SUPPORTED_LANGUAGES = [
    "python",
    "javascript",
    "typescript",
    "java",
    "cpp",
    "c",
    "csharp",
    "go",
    "rust",
    "php",
    "ruby",
    "swift",
    "kotlin",
    "sql",
    "html",
    "css",
    "json",
    "yaml",
    "shell",
    "r",
    "dart",
]

LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "c",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".sql": "sql",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "css",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "shell",
    ".bash": "shell",
    ".r": "r",
    ".dart": "dart",
}

EXPLANATION_MODES = [
    "overview",
    "line_by_line",
    "beginner",
    "advanced",
    "security",
    "refactor",
]

MODE_DISPLAY_NAMES = {
    "overview": "Overview",
    "line_by_line": "Line-by-Line",
    "beginner": "Beginner",
    "advanced": "Advanced",
    "security": "Security Audit",
    "refactor": "Refactor Suggestions",
}

KEYRING_SERVICE_NAME = "codelens"
KEYRING_GEMINI_API_KEY = "gemini_api_key"
KEYRING_OPENAI_API_KEY = "openai_api_key"
KEYRING_CLAUDE_API_KEY = "claude_api_key"

DB_NAME = "codelens.db"
MAX_HISTORY_ITEMS = 20

WINDOW_MIN_WIDTH = 1100
WINDOW_MIN_HEIGHT = 700
WINDOW_DEFAULT_WIDTH = 1400
WINDOW_DEFAULT_HEIGHT = 900

FONT_SIZE_MIN = 10
FONT_SIZE_MAX = 22
FONT_SIZE_DEFAULT = 13

MONOSPACE_FONTS = ["JetBrains Mono", "Fira Code", "Consolas", "Courier New"]

TOKEN_ESTIMATE_CHARS_PER_TOKEN = 4
