# Contributing to CodeLens

Thank you for your interest in contributing to CodeLens! This document provides guidelines and instructions for contributing to the project.

---

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, gender identity, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project team at conduct@codelens.dev. All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 Getting Started

### Development Environment Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/codelens.git
   cd codelens
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate it
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Install runtime dependencies
   pip install -r requirements.txt

   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

---

## 🌿 Branch Naming Convention

Use descriptive branch names that follow this pattern:

- `feature/short-description` - For new features
- `fix/short-description` - For bug fixes
- `chore/short-description` - For maintenance tasks
- `docs/short-description` - For documentation updates
- `refactor/short-description` - For code refactoring

**Examples:**
- `feature/add-snippet-export`
- `fix/chat-history-bug`
- `chore/update-dependencies`
- `docs/improve-readme`

---

## 💬 Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat` - A new feature
- `fix` - A bug fix
- `docs` - Documentation only changes
- `style` - Code style changes (formatting, missing semi-colons, etc.)
- `refactor` - Code change that neither fixes a bug nor adds a feature
- `perf` - Performance improvements
- `test` - Adding or updating tests
- `chore` - Maintenance tasks, dependency updates

### Examples

```
feat(chat): add message export functionality

Added ability to export chat history to text file.
Users can now click "Export Chat" button to save conversations.

Closes #123
```

```
fix(editor): resolve syntax highlighting crash on large files

Fixed issue where files over 10MB would cause the syntax
highlighter to freeze the application.

Fixes #456
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_language_detector.py

# Run specific test
pytest tests/test_language_detector.py::TestLanguageDetector::test_detect_python_from_extension
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what is being tested
- Mock external dependencies (API calls, file system, etc.)
- Aim for high test coverage (>80%)

**Example test:**

```python
def test_language_detector_identifies_python():
    """Test that Python code is correctly identified"""
    code = "def hello(): print('world')"
    result = LanguageDetector.detect_from_content(code)
    assert result == "python"
```

---

## 🎨 Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length:** 100 characters (not 79)
- **Indentation:** 4 spaces
- **Quotes:** Double quotes for strings
- **Imports:** Grouped and sorted (stdlib, third-party, local)

### Formatting with Black

```bash
# Format all Python files
black app/ tests/

# Check formatting without making changes
black --check app/ tests/
```

### Type Checking with mypy

```bash
# Run type checker
mypy app/

# Type hints are required for:
# - All function signatures
# - Class attributes
# - Complex variables
```

### Linting with flake8

```bash
# Run linter
flake8 app/ tests/

# Fix common issues automatically
autopep8 --in-place --recursive app/ tests/
```

---

## 📝 Documentation

### Code Documentation

- **Docstrings:** All modules, classes, and functions must have docstrings
- **Format:** Use Google-style docstrings
- **Type hints:** Include type hints in function signatures

**Example:**

```python
def explain_code(code: str, language: str, mode: str) -> str:
    """
    Generate an AI explanation for the given code.

    Args:
        code: The source code to explain
        language: Programming language (e.g., "python", "javascript")
        mode: Explanation mode (e.g., "overview", "beginner")

    Returns:
        The generated explanation text

    Raises:
        ValueError: If mode is not recognized
        APIError: If the AI service fails
    """
    pass
```

### README Updates

- Update README.md if you add new features
- Include screenshots for UI changes
- Update the feature list and usage guide

---

## 🔍 Pull Request Process

### Before Submitting

1. **Ensure all tests pass**
   ```bash
   pytest
   ```

2. **Format your code**
   ```bash
   black app/ tests/
   ```

3. **Run type checker**
   ```bash
   mypy app/
   ```

4. **Run linter**
   ```bash
   flake8 app/ tests/
   ```

5. **Update documentation** if needed

### PR Checklist

- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`black`)
- [ ] Type checking passes (`mypy`)
- [ ] Linting passes (`flake8`)
- [ ] Documentation updated (if applicable)
- [ ] README updated (if adding features)
- [ ] Commit messages follow Conventional Commits
- [ ] Branch name follows naming convention
- [ ] PR description explains the changes

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes.

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Tests pass
- [ ] Code formatted with black
- [ ] mypy passes
- [ ] flake8 passes
- [ ] Documentation updated
```

---

## 🐛 Reporting Bugs

### Before Reporting

1. Check if the bug has already been reported in [Issues](https://github.com/codelens/codelens/issues)
2. Try to reproduce the bug with the latest version
3. Gather relevant information (OS, Python version, error messages)

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- Python version: [e.g., 3.11.5]
- CodeLens version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

---

## 💡 Suggesting Features

We welcome feature suggestions! Please:

1. Check if the feature has already been requested
2. Explain the use case and benefits
3. Provide examples or mockups if possible

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Mockups, examples, or other relevant information.
```

---

## 📦 Release Process

(For maintainers)

1. Update version in `app/config/constants.py`
2. Update CHANGELOG.md
3. Create a git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions will build and create a release

---

## 🤝 Community

- **GitHub Discussions** - Ask questions, share ideas
- **Discord** - Real-time chat with contributors
- **Twitter** - Follow [@CodeLensApp](https://twitter.com/codelensapp) for updates

---

## 📧 Contact

- **Maintainers** - maintainers@codelens.dev
- **Security Issues** - security@codelens.dev (for responsible disclosure)

---

Thank you for contributing to CodeLens! 🎉

*Last updated: 2026*
