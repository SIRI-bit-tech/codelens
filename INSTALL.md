# CodeLens Installation Guide

Complete installation instructions for all platforms.

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 11+, or Linux (Ubuntu 20.04+)
- **Python**: 3.9 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for installation
- **Internet**: Required for AI explanations

### Recommended Requirements
- **OS**: Windows 11, macOS 13+, or Ubuntu 22.04+
- **Python**: 3.11 or higher
- **RAM**: 8GB
- **Disk Space**: 1GB
- **Display**: 1920×1080 or higher

---

## Installation Methods

### Method 1: Pre-built Executables (Recommended for Users)

#### Windows

1. Download `CodeLens-Setup.exe` from [Releases](https://github.com/codelens/codelens/releases)
2. Double-click the installer
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

#### macOS

1. Download `CodeLens.dmg` from [Releases](https://github.com/codelens/codelens/releases)
2. Open the DMG file
3. Drag CodeLens to Applications folder
4. Right-click CodeLens in Applications and select "Open" (first time only)
5. Click "Open" in the security dialog

#### Linux

1. Download `CodeLens.AppImage` from [Releases](https://github.com/codelens/codelens/releases)
2. Make it executable:
   ```bash
   chmod +x CodeLens.AppImage
   ```
3. Run it:
   ```bash
   ./CodeLens.AppImage
   ```

---

### Method 2: From Source (Recommended for Developers)

#### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/codelens/codelens.git
cd codelens
```

#### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5: Run Application

```bash
python main.py
```

---

### Method 3: Using pip (Future Release)

```bash
pip install codelens
codelens
```

*(Not yet available - coming soon)*

---

## Post-Installation Setup

### 1. Get Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"** in the top navigation
4. Click **"Create API Key"**
5. Copy the generated API key

### 2. Configure CodeLens

1. Launch CodeLens
2. Click **⚙️ Settings** button in the toolbar
3. Paste your API key in the "Google Gemini API Key" field
4. (Optional) Adjust other settings:
   - Theme (Light/Dark/System)
   - Font size
   - Default explanation mode
   - Enable/disable streaming
5. Click **Save**

### 3. Verify Installation

1. Paste this test code in the editor:
   ```python
   def greet(name):
       return f"Hello, {name}!"
   
   print(greet("World"))
   ```

2. Click **⚡ Explain**

3. You should see an explanation appear in the right panel

4. Try asking a follow-up question in the chat: "What does the f-string do?"

---

## Troubleshooting

### Windows Issues

#### "Python is not recognized"
**Solution:**
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Or manually add Python to PATH:
   - Search "Environment Variables" in Start Menu
   - Edit "Path" variable
   - Add Python installation directory

#### "DLL load failed"
**Solution:**
```bash
pip install --upgrade --force-reinstall PyQt6
```

#### Antivirus blocks executable
**Solution:**
- Add CodeLens to antivirus exceptions
- Or run from source instead

### macOS Issues

#### "CodeLens is damaged and can't be opened"
**Solution:**
```bash
xattr -cr /Applications/CodeLens.app
```

#### "CodeLens can't be opened because Apple cannot check it"
**Solution:**
1. Right-click CodeLens in Applications
2. Select "Open"
3. Click "Open" in the dialog

#### Permission denied
**Solution:**
```bash
chmod +x CodeLens.app/Contents/MacOS/CodeLens
```

### Linux Issues

#### "No module named 'PyQt6'"
**Solution:**
```bash
sudo apt install python3-pyqt6
# Or
pip install PyQt6
```

#### "libxcb-xinerama.so.0: cannot open shared object file"
**Solution:**
```bash
sudo apt install libxcb-xinerama0
```

#### AppImage won't run
**Solution:**
```bash
# Install FUSE
sudo apt install fuse libfuse2

# Make executable
chmod +x CodeLens.AppImage

# Run
./CodeLens.AppImage
```

### API Issues

#### "Please add your API key"
**Solution:**
- Get API key from [aistudio.google.com](https://aistudio.google.com)
- Add it in Settings (⚙️)

#### "API key is invalid"
**Solution:**
- Verify you copied the entire key
- Create a new key if needed
- Check for extra spaces

#### "Cannot reach the API"
**Solution:**
- Check internet connection
- Verify firewall isn't blocking the app
- Try again in a few minutes (rate limiting)

### General Issues

#### Application won't start
**Solution:**
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Run with verbose output
python main.py --verbose
```

#### Slow performance
**Solution:**
- Disable streaming in Settings
- Close other applications
- Check system resources

#### Database errors
**Solution:**
```bash
# Delete database and restart
# Windows:
del %USERPROFILE%\.codelens\codelens.db

# macOS/Linux:
rm ~/.codelens/codelens.db
```

---

## Uninstallation

### Windows
1. Open "Add or Remove Programs"
2. Find "CodeLens"
3. Click "Uninstall"

Or manually:
1. Delete installation folder
2. Delete `%USERPROFILE%\.codelens`

### macOS
1. Drag CodeLens from Applications to Trash
2. Delete `~/.codelens` folder

### Linux
1. Delete the AppImage file
2. Delete `~/.codelens` folder

### From Source
```bash
# Deactivate virtual environment
deactivate

# Delete project folder
rm -rf codelens/
```

---

## Updating

### Pre-built Executables
1. Download new version
2. Install over existing version
3. Settings and history are preserved

### From Source
```bash
cd codelens
git pull origin main
pip install --upgrade -r requirements.txt
python main.py
```

---

## Verification Checklist

After installation, verify:

- [ ] Application launches without errors
- [ ] Settings dialog opens (⚙️)
- [ ] API key can be saved
- [ ] Code editor accepts input
- [ ] File can be opened (📂)
- [ ] Language detection works
- [ ] Explanation generates successfully
- [ ] Chat responds to questions
- [ ] Theme can be changed
- [ ] History saves and loads
- [ ] Export to Markdown works

---

## Getting Help

If you encounter issues not covered here:

1. **Check Documentation**
   - [README.md](README.md)
   - [QUICKSTART.md](QUICKSTART.md)
   - [FAQ](#) (coming soon)

2. **Search Issues**
   - [GitHub Issues](https://github.com/codelens/codelens/issues)

3. **Ask for Help**
   - [GitHub Discussions](https://github.com/codelens/codelens/discussions)
   - Email: support@codelens.dev

4. **Report a Bug**
   - [Create an Issue](https://github.com/codelens/codelens/issues/new)

---

## System-Specific Notes

### Windows
- Requires Windows 10 version 1809 or later
- Windows Defender may scan the executable on first run
- Portable mode: Run from USB drive (settings stored locally)

### macOS
- Requires macOS 11 (Big Sur) or later
- Apple Silicon (M1/M2) and Intel both supported
- Gatekeeper may require manual approval on first run

### Linux
- Tested on Ubuntu 20.04+, Fedora 35+, Arch Linux
- Wayland and X11 both supported
- May require additional Qt dependencies

---

*Last updated: 2026-05-01*
*Version: 1.0.0*
