# Quick Release Guide for CodeLens

## Do I need to push to GitHub first?

**Short answer: No, but it's recommended.**

- You can build the `.exe` locally and share it directly (email, Google Drive, etc.)
- GitHub releases make it easier to distribute and track versions
- Users can download directly from GitHub

---

## Option 1: Quick Local Build (No GitHub)

If you just want to create an executable to share:

```bash
# 1. Build the executable
pyinstaller codelens.spec

# 2. Your executable is ready!
# Location: dist/CodeLens.exe

# 3. Share it however you want:
# - Email
# - Google Drive
# - Dropbox
# - USB drive
```

**That's it!** No GitHub needed.

---

## Option 2: GitHub Release (Recommended)

### Step 1: Build Locally

```bash
# Make sure you're in the CodeLens directory
cd D:\FILES\FILEZ\CodeLens

# Activate virtual environment
venv\Scripts\activate

# Build the executable
pyinstaller codelens.spec

# Your executable is now in: dist/CodeLens.exe
```

### Step 2: Push to GitHub

```bash
# Add all changes
git add .

# Commit with a message
git commit -m "Release v1.0.0 - Rate limiting and UI improvements"

# Push to GitHub
git push origin main
```

### Step 3: Create a Tag

```bash
# Create a version tag
git tag v1.0.0

# Push the tag to GitHub
git push origin v1.0.0
```

### Step 4: Create Release on GitHub

**Method A: Using GitHub Website**

1. Go to your repository: `https://github.com/YOUR_USERNAME/CodeLens`
2. Click **"Releases"** (on the right side)
3. Click **"Draft a new release"**
4. Click **"Choose a tag"** → Select `v1.0.0`
5. **Release title**: Type `CodeLens v1.0.0`
6. **Description**: Add what's new:
   ```
   ## What's New
   - Added rate limiting to prevent API quota issues
   - Improved chat UI with better readability
   - Fixed retry logic for rate limit errors
   
   ## Download
   Download CodeLens.exe below and run it!
   ```
7. **Attach files**: Drag `dist/CodeLens.exe` into the box
8. Click **"Publish release"**

**Method B: Using GitHub CLI (Faster)**

```bash
# Install GitHub CLI first: https://cli.github.com/
# Then run:

gh release create v1.0.0 dist/CodeLens.exe \
  --title "CodeLens v1.0.0" \
  --notes "Rate limiting and UI improvements. Download and run!"
```

---

## What Users See

After creating a release, users can:

1. Go to your GitHub repository
2. Click "Releases"
3. See "CodeLens v1.0.0"
4. Click "CodeLens.exe" to download
5. Run it directly (no installation needed)

---

## Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- `v1.0.0` - First release
- `v1.0.1` - Bug fix
- `v1.1.0` - New feature
- `v2.0.0` - Major changes

Examples:
- Fixed a bug? → `v1.0.1`
- Added chat feature? → `v1.1.0`
- Complete redesign? → `v2.0.0`

---

## Quick Commands Reference

```bash
# Build executable
pyinstaller codelens.spec

# Commit and push
git add .
git commit -m "Your message"
git push origin main

# Create and push tag
git tag v1.0.0
git push origin v1.0.0

# Create release with GitHub CLI
gh release create v1.0.0 dist/CodeLens.exe --title "v1.0.0" --notes "Release notes"
```

---

## Troubleshooting

**Q: I don't have GitHub CLI**
- **A**: Use the GitHub website method instead, or install from https://cli.github.com/

**Q: My executable doesn't work on other computers**
- **A**: Make sure you built with PyInstaller (not just running `python main.py`)

**Q: Users get "Windows protected your PC" warning**
- **A**: Normal for unsigned apps. Tell users to click "More info" → "Run anyway"

**Q: How do I update a release?**
- **A**: Create a new tag (v1.0.1) and new release. Don't edit old releases.

---

## Next Steps

After your first release:

1. Update `CHANGELOG.md` with changes
2. Update version in `app/config/constants.py`
3. Test the executable on a clean Windows machine
4. Share the GitHub release link with users

---

*Need help? Check DEPLOYMENT.md for detailed instructions.*
