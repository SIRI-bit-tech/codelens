# CodeLens Deployment Guide

This guide covers building and deploying CodeLens for Windows, macOS, and Linux.

---

## Quick Answer: GitHub Release Process

**Do you need to push to GitHub first?**
- **No, you don't HAVE to**, but it's recommended for version control and backup
- You can build locally and distribute the executables directly
- GitHub releases are optional but make distribution easier

**How to create a GitHub release:**

1. **Commit and push your code**:
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   git push origin main
   ```

2. **Create and push a tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Create release on GitHub**:
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Select the tag you just created (v1.0.0)
   - Add release title: "CodeLens v1.0.0"
   - Add release notes describing changes
   - Upload your built executables (CodeLens.exe, CodeLens.dmg, etc.)
   - Click "Publish release"

**OR use GitHub CLI** (faster):
```bash
# Install GitHub CLI first: https://cli.github.com/
gh release create v1.0.0 dist/CodeLens.exe --title "CodeLens v1.0.0" --notes "Initial release"
```

---

## Prerequisites

- Python 3.9 or higher
- PyInstaller (`pip install pyinstaller`)
- Platform-specific tools (see below)

---

## Building Executables

### 1. Prepare the Environment

```bash
# Clone the repository
git clone https://github.com/codelens/codelens.git
cd codelens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Build with PyInstaller

```bash
# Build for current platform
pyinstaller codelens.spec

# Output will be in dist/ directory
```

---

## Platform-Specific Instructions

### Windows

#### Building

```bash
# Activate virtual environment
venv\Scripts\activate

# Build executable
pyinstaller codelens.spec

# Output: dist/CodeLens.exe
```

#### Creating Installer with Inno Setup

1. **Install Inno Setup**
   - Download from https://jrsoftware.org/isdl.php
   - Install to default location

2. **Create installer script** (`installer.iss`):

```inno
[Setup]
AppName=CodeLens
AppVersion=1.0.0
DefaultDirName={pf}\CodeLens
DefaultGroupName=CodeLens
OutputDir=dist
OutputBaseFilename=CodeLens-Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\CodeLens.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CodeLens"; Filename: "{app}\CodeLens.exe"
Name: "{commondesktop}\CodeLens"; Filename: "{app}\CodeLens.exe"

[Run]
Filename: "{app}\CodeLens.exe"; Description: "Launch CodeLens"; Flags: postinstall nowait skipifsilent
```

3. **Compile installer**:
   ```bash
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
   ```

4. **Output**: `dist/CodeLens-Setup.exe`

---

### macOS

#### Building

```bash
# Activate virtual environment
source venv/bin/activate

# Build app bundle
pyinstaller codelens.spec

# Output: dist/CodeLens.app
```

#### Creating DMG

1. **Install dmgbuild**:
   ```bash
   pip install dmgbuild
   ```

2. **Create DMG settings** (`dmg_settings.py`):

```python
import os

application = "dist/CodeLens.app"
appname = "CodeLens"

format = "UDBZ"
size = "200M"

files = [application]
symlinks = {"Applications": "/Applications"}

icon_locations = {
    appname + ".app": (100, 100),
    "Applications": (400, 100),
}

background = "builtin-arrow"

window_rect = ((100, 100), (500, 300))
icon_size = 128
text_size = 16
```

3. **Build DMG**:
   ```bash
   dmgbuild -s dmg_settings.py "CodeLens" dist/CodeLens.dmg
   ```

4. **Output**: `dist/CodeLens.dmg`

#### Code Signing (Optional)

```bash
# Sign the app
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/CodeLens.app

# Verify signature
codesign --verify --deep --strict --verbose=2 dist/CodeLens.app
```

---

### Linux

#### Building

```bash
# Activate virtual environment
source venv/bin/activate

# Build executable
pyinstaller codelens.spec

# Output: dist/CodeLens
```

#### Creating AppImage

1. **Download appimagetool**:
   ```bash
   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
   chmod +x appimagetool-x86_64.AppImage
   ```

2. **Create AppDir structure**:
   ```bash
   mkdir -p CodeLens.AppDir/usr/bin
   mkdir -p CodeLens.AppDir/usr/share/applications
   mkdir -p CodeLens.AppDir/usr/share/icons/hicolor/512x512/apps

   # Copy executable
   cp dist/CodeLens CodeLens.AppDir/usr/bin/

   # Create desktop file
   cat > CodeLens.AppDir/usr/share/applications/codelens.desktop << EOF
   [Desktop Entry]
   Type=Application
   Name=CodeLens
   Exec=CodeLens
   Icon=codelens
   Categories=Development;
   EOF

   # Copy icon (if available)
   cp assets/icons/app_icon.png CodeLens.AppDir/usr/share/icons/hicolor/512x512/apps/codelens.png

   # Create AppRun script
   cat > CodeLens.AppDir/AppRun << 'EOF'
   #!/bin/bash
   SELF=$(readlink -f "$0")
   HERE=${SELF%/*}
   export PATH="${HERE}/usr/bin:${PATH}"
   exec "${HERE}/usr/bin/CodeLens" "$@"
   EOF

   chmod +x CodeLens.AppDir/AppRun
   ```

3. **Build AppImage**:
   ```bash
   ./appimagetool-x86_64.AppImage CodeLens.AppDir CodeLens.AppImage
   ```

4. **Output**: `CodeLens.AppImage`

---

## GitHub Actions Automated Builds

The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically:

1. Runs tests on all platforms
2. Builds executables on push to main
3. Creates release artifacts on tagged releases

### Manual Release Process (Step-by-Step)

**Option 1: Using GitHub Web Interface**

1. **Build your executables locally**:
   ```bash
   # Windows
   pyinstaller codelens.spec
   # Creates: dist/CodeLens.exe
   ```

2. **Commit and push your code**:
   ```bash
   git add .
   git commit -m "Release v1.0.0 - Added rate limiting and improved chat UI"
   git push origin main
   ```

3. **Create a tag**:
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin v1.0.0
   ```

4. **Create release on GitHub**:
   - Go to `https://github.com/YOUR_USERNAME/CodeLens/releases`
   - Click **"Draft a new release"**
   - Click **"Choose a tag"** → Select `v1.0.0`
   - **Release title**: `CodeLens v1.0.0`
   - **Description**: Add release notes (what's new, bug fixes, etc.)
   - **Attach files**: Drag and drop your `dist/CodeLens.exe` (or .dmg, .AppImage)
   - Click **"Publish release"**

**Option 2: Using GitHub CLI (Recommended - Faster)**

```bash
# Install GitHub CLI first: https://cli.github.com/

# Login to GitHub
gh auth login

# Build your executable
pyinstaller codelens.spec

# Create release and upload files in one command
gh release create v1.0.0 \
  dist/CodeLens.exe \
  --title "CodeLens v1.0.0" \
  --notes "## What's New
- Added rate limiting to prevent API quota exhaustion
- Improved chat bubble styling for better readability
- Fixed retry logic with exponential backoff

## Download
Download CodeLens.exe below and run it on Windows."
```

**Option 3: Automated with GitHub Actions**

If you have GitHub Actions set up (`.github/workflows/ci.yml`):

```bash
# Just tag and push - GitHub Actions does the rest
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# - Run tests
# - Build for Windows, macOS, Linux
# - Create release with all binaries
```

---

### Release Notes Template

When creating a release, use this template:

```markdown
## 🎉 What's New

- Added rate limiting (4 seconds between requests) to prevent API quota issues
- Improved chat bubble UI with better contrast and readability
- Added automatic retry logic with exponential backoff for rate limit errors

## 🐛 Bug Fixes

- Fixed 429 RESOURCE_EXHAUSTED errors on startup
- Fixed dark theme chat bubbles with poor text visibility

## 📥 Installation

1. Download `CodeLens.exe` below
2. Run the executable (no installation required)
3. Add your Google Gemini API key in Settings

## 🔧 Requirements

- Windows 10 or higher
- Google Gemini API key (free tier available)

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.
```

---

## Distribution Checklist

Before distributing a new version:

- [ ] Update version in `app/config/constants.py`
- [ ] Update `README.md` with new features
- [ ] Update `CHANGELOG.md`
- [ ] Run all tests: `pytest`
- [ ] Build for all platforms
- [ ] Test executables on clean systems
- [ ] Create GitHub release with binaries
- [ ] Update website/documentation

---

## Troubleshooting

### Windows

**Issue**: Missing DLL errors
- **Solution**: Ensure all dependencies are included in `codelens.spec`

**Issue**: Antivirus flags executable
- **Solution**: Sign the executable with a code signing certificate

### macOS

**Issue**: "App is damaged" error
- **Solution**: Sign the app with a Developer ID certificate

**Issue**: Gatekeeper blocks app
- **Solution**: Notarize the app with Apple

### Linux

**Issue**: Missing libraries
- **Solution**: Use AppImage which bundles all dependencies

**Issue**: Permission denied
- **Solution**: Make AppImage executable: `chmod +x CodeLens.AppImage`

---

## Code Signing

### Windows

1. Obtain a code signing certificate
2. Sign the executable:
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/CodeLens.exe
   ```

### macOS

1. Enroll in Apple Developer Program
2. Create Developer ID certificate
3. Sign and notarize:
   ```bash
   codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/CodeLens.app
   xcrun notarytool submit dist/CodeLens.dmg --apple-id your@email.com --password app-specific-password --team-id TEAMID
   ```

---

## Continuous Deployment

For automated deployment:

1. Set up GitHub Actions secrets:
   - `WINDOWS_CERT` - Windows code signing certificate
   - `MACOS_CERT` - macOS Developer ID certificate
   - `APPLE_ID` - Apple ID for notarization

2. Update `.github/workflows/ci.yml` to include signing steps

3. Releases will be automatically built and signed on tag push

---

*Last updated: 2026*
