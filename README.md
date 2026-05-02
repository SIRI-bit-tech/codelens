# CodeLens - AI-Powered Code Explainer

![CodeLens Banner](https://github.com/user-attachments/assets/3907abea-ffb0-47b6-8456-9e4390d89aa4)

## What is CodeLens?

**CodeLens** is a powerful desktop application that helps developers understand code instantly using AI. Whether you're a junior developer learning a new language, a student working through coding bootcamps, or an experienced programmer exploring unfamiliar codebases, CodeLens provides clear, structured explanations in seconds.

Simply paste or open any code file, select an explanation mode (Overview, Line-by-Line, Beginner, Advanced, Security Audit, or Refactor Suggestions), and get instant AI-powered insights. CodeLens also features an interactive chat interface where you can ask follow-up questions about the code, making it your personal coding tutor available 24/7.

---

## ✨ Features

- 🤖 **AI-Powered Explanations** - Powered by Google Gemini 2.0 Flash (free tier)
- 📝 **6 Explanation Modes** - Overview, Line-by-Line, Beginner, Advanced, Security, Refactor
- 💬 **Interactive Chat** - Ask follow-up questions about the code
- 🎨 **Syntax Highlighting** - Beautiful code editor with line numbers
- 🌓 **Dark & Light Themes** - Easy on the eyes, day or night
- 📚 **20+ Languages Supported** - Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- 💾 **History & Snippets** - Save and reload past explanations and code snippets
- 📤 **Export Options** - Save explanations as Markdown or PDF
- ⚡ **Real-time Streaming** - See explanations appear as they're generated
- 🔒 **Secure** - API keys stored securely in system keyring
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux

---

## 📸 Screenshots

### Main Interface - Code Explanation
![Main Interface](https://github.com/user-attachments/assets/3907abea-ffb0-47b6-8456-9e4390d89aa4)

### Interactive Chat Interface
![Chat Interface](https://github.com/user-attachments/assets/7a5ccd22-af85-44a0-bdfa-8c9b0d346f61)

### Settings
![Settings](https://github.com/user-attachments/assets/904abd9f-bc13-405b-979c-1fcb3b48f50b)

---

## 📥 Installation

### Windows

1. **Download** `CodeLens-Windows.exe` from the [latest release](https://github.com/SIRI-bit-tech/codelens/releases/tag/v1.0.0)
2. **Run** the executable (no installation needed)
3. **Add your API key** in Settings (⚙️)

### macOS

1. **Download** `CodeLens-macOS.app` from the [latest release](https://github.com/SIRI-bit-tech/codelens/releases/tag/v1.0.0)
2. **Open** the app (you may need to right-click → Open first time due to Gatekeeper)
3. **Add your API key** in Settings (⚙️)

### Linux

1. **Download** `CodeLens-Linux` from the [latest release](https://github.com/SIRI-bit-tech/codelens/releases/tag/v1.0.0)
2. **Make it executable**: `chmod +x CodeLens-Linux`
3. **Run**: `./CodeLens-Linux`
4. **Add your API key** in Settings (⚙️)

No Python, no dependencies, just download and run!

### From Source (For Developers)

```bash
# Clone the repository
git clone https://github.com/SIRI-bit-tech/codelens.git
cd codelens

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🔑 Getting an API Key

CodeLens uses Google's Gemini API (free tier) for AI explanations. Here's how to get your API key:

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"** in the top right
4. Click **"Create API Key"**
5. Copy your API key
6. In CodeLens, click **⚙️ Settings**
7. Paste your API key in the "Google Gemini API Key" field
8. Click **Save**

**Note:** The free tier includes:
- 15 requests per minute
- 1 million tokens per minute
- 1,500 requests per day

This is more than enough for typical usage!

---

## 📖 Usage Guide

### Explaining Code

1. **Paste or Open Code**
   - Paste code directly into the left editor panel, OR
   - Click **📂 Open File** to load a code file from disk

2. **Select Language** (optional)
   - CodeLens auto-detects the language
   - You can manually override using the **Language** dropdown

3. **Choose Explanation Mode**
   - **Overview** - High-level summary of what the code does
   - **Line-by-Line** - Detailed walkthrough of each line
   - **Beginner** - Simple explanations with analogies (no jargon)
   - **Advanced** - Technical analysis with Big-O, design patterns
   - **Security** - Security audit highlighting vulnerabilities
   - **Refactor** - Suggestions for improving code quality

4. **Click ⚡ Explain**
   - Watch the explanation appear in real-time (if streaming is enabled)
   - The explanation appears in the right panel with formatted markdown

5. **Ask Follow-up Questions**
   - Use the chat panel below the explanation
   - Ask things like "What does line 12 do?" or "Why use a dictionary here?"
   - CodeLens remembers the context of your code and explanation

### Saving & Exporting

- **Copy Explanation** - Click **📋 Copy** to copy to clipboard
- **Save as Text** - Click **💾 Save as TXT**
- **Save as Markdown** - Click **💾 Save as MD**
- **Export Session** - Export code + explanation + chat as PDF or Markdown

### Managing History

- View past explanations in the **History** panel
- Click any entry to reload it
- Delete entries you no longer need

### Code Snippets

- Save frequently used code snippets
- Tag and search your snippet library
- Load snippets with one click

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Explain code |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save explanation |
| `Ctrl+L` | Clear all |
| `Ctrl+,` | Open settings |

---

## 🌐 Supported Languages

Python • JavaScript • TypeScript • Java • C++ • C • C# • Go • Rust • PHP • Ruby • Swift • Kotlin • SQL • HTML • CSS • JSON • YAML • Shell • R • Dart

---

## ⚙️ Configuration

### Settings

Access settings via **⚙️ Settings** button or `Ctrl+,`:

- **API Key** - Your Google Gemini API key (stored securely)
- **Theme** - Light, Dark, or System
- **Font Size** - Adjust editor and explanation text size (10-22)
- **Default Mode** - Your preferred explanation mode
- **Stream Responses** - Enable/disable real-time streaming
- **Auto-detect Language** - Automatically detect programming language
- **Save History** - Save explanations to local database

### Privacy

⚠️ **Important:** Your code is sent to Google's Gemini API for explanation. CodeLens does not store your code on any remote server—only locally in SQLite. See [Google's Privacy Policy](https://policies.google.com/privacy) for details on how Google handles data.

---

## 🛠️ Building from Source

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Development Setup

```bash
# Clone the repository
git clone https://github.com/SIRI-bit-tech/codelens.git
cd codelens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Code Quality

```bash
# Format code with black
black app/ tests/

# Type checking with mypy
mypy app/

# Linting with flake8
flake8 app/ tests/
```

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_language_detector.py
```

---

## 📦 Building Executables

### Windows

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller codelens.spec

# Executable will be in dist/CodeLens.exe
```

### macOS

```bash
# Install PyInstaller
pip install pyinstaller

# Build app bundle
pyinstaller codelens.spec

# App will be in dist/CodeLens.app
```

### Linux

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller codelens.spec

# Executable will be in dist/CodeLens
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](https://github.com/SIRI-bit-tech/codelens/blob/main/CONTRIBUTING.md) for guidelines.

---

## 📄 License

CodeLens is licensed under the [MIT License](https://github.com/SIRI-bit-tech/codelens/blob/main/LICENSE).

---

## 🙏 Acknowledgements

- **Google Gemini** - AI-powered code explanations
- **PyQt6** - Cross-platform GUI framework
- **QScintilla** - Syntax highlighting editor component
- **Pygments** - Syntax highlighting library
- **ReportLab** - PDF generation
- **Keyring** - Secure credential storage

---

## 📞 Support

- **Issues** - [GitHub Issues](https://github.com/SIRI-bit-tech/codelens/issues)
- **Discussions** - [GitHub Discussions](https://github.com/SIRI-bit-tech/codelens/discussions)
- **Download** - [Latest Release](https://github.com/SIRI-bit-tech/codelens/releases/tag/v1.0.0)
- **Email** - [Email](siritech001@gmail.com)
---

**Made with ❤️ by the SIRIDEV**

*Version 1.0.0 | Last Updated: 2026*
