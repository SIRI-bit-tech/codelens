# Changelog

All notable changes to CodeLens will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-05-01

### Added

#### Core Features
- AI-powered code explanations using Google Gemini 2.0 Flash
- 6 explanation modes: Overview, Line-by-Line, Beginner, Advanced, Security Audit, Refactor Suggestions
- Interactive follow-up chat with context awareness
- Syntax-highlighted code editor with line numbers
- Real-time streaming responses
- Support for 20+ programming languages

#### UI/UX
- Dark and light themes with system theme detection
- Resizable split-pane layout
- Custom status bar showing language, token count, and connection status
- Loading spinner for API requests
- Markdown rendering for explanations with syntax highlighting

#### Data Management
- Local SQLite database for history storage
- History panel showing last 20 explanations
- Code snippet library with search and tags
- Export sessions to Markdown or PDF

#### Settings
- Secure API key storage using system keyring
- Configurable font size (10-22)
- Toggle streaming responses
- Auto-detect programming language
- Default explanation mode selector

#### Developer Features
- Comprehensive test suite with pytest
- Type checking with mypy
- Code formatting with black
- Linting with flake8
- GitHub Actions CI/CD pipeline

#### Documentation
- Complete README with installation instructions
- CONTRIBUTING guide with code of conduct
- DEPLOYMENT guide for all platforms
- QUICKSTART guide for new users
- Inline code documentation with docstrings

#### Keyboard Shortcuts
- `Ctrl+Enter` - Explain code
- `Ctrl+O` - Open file
- `Ctrl+S` - Save explanation
- `Ctrl+L` - Clear all
- `Ctrl+,` - Open settings

### Security
- API keys stored securely in system keyring (never in plaintext)
- No remote storage of user code (local SQLite only)
- HTML sanitization in explanation panel

---

## [Unreleased]

### Planned Features
- Multi-file project analysis
- Code comparison mode
- Custom prompt templates
- Plugin system for extensions
- Collaborative features (share explanations)
- Offline mode with cached responses
- More export formats (HTML, DOCX)
- Syntax highlighting themes
- Code execution sandbox
- Integration with popular IDEs

---

[1.0.0]: https://github.com/codelens/codelens/releases/tag/v1.0.0
