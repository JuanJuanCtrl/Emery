# 🚀 Quick Start Guide

Get up and running with Emery in 5 minutes.

## Installation

```bash
# Clone the repository
git clone https://github.com/JuanJuanCtrl/Emery.git
cd Emery

# Install dependencies
pip install -e .
```

That's it! The `emery` command is now available in your terminal.

## Basic Usage

### 1. Upload a single file

```bash
emery upload document.pdf
```

This will:
- ✓ Validate the file
- ✓ Copy it to the `files/` directory
- ✓ Create/switch to the `files` branch
- ✓ Commit with auto-generated message
- ✓ Push to remote
- ✓ Return to main branch

### 2. Upload multiple files at once

```bash
emery upload file1.txt file2.pdf presentation.pptx
```

### 3. Add a custom commit message

```bash
emery upload -m "Add Q1 2026 financial reports" sales.xlsx quarterly_summary.pdf
```

### 4. Copy files without git operations (dry run)

```bash
emery upload --no-commit huge_file.zip
```

Later, manually commit if you want:
```bash
cd files/
git add .
git commit -m "Add large files"
git push
```

### 5. View configuration and uploaded files

```bash
emery info
```

Shows:
- Maximum file size (100 MB default)
- Target branch (files)
- Upload directory location
- Files currently in the upload directory

### 6. Clear uploaded files

```bash
emery clean
```

>  **Warning**: This removes all files in the upload directory but doesn't affect git history.

## Drag & Drop (Terminal)

Most modern terminals support dragging files:

1. Open Emery:
   ```bash
   emery upload
   ```

2. Drag your files into the terminal window

3. Press Enter

## Configuration

Edit `emery_cli/config.py` to customize:

```python
MAX_FILE_SIZE_MB = 100      # Max file size in MB
TARGET_BRANCH = "files"      # Git branch for uploads
GIT_AUTHOR_NAME = "Name"     # Commit author
GIT_AUTHOR_EMAIL = "email"   # Commit author email
```

Or set environment variables:
```bash
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your@email.com"
```

## Workflow at a Glance

```
┌─────────────┐
│ Run emery   │
│   upload    │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│  Validate    │
│  file size   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Copy file   │
│  to files/   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Switch to   │ (auto-commit enabled)
│  files/      │
│  branch      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Commit &    │
│  push to     │
│  remote      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Return to   │
│  main branch │
└──────────────┘
```

## Tips & Tricks

### Batch uploads for efficiency
```bash
# Upload many files at once - faster than individual uploads
emery upload *.pdf *.xlsx documents/*.txt
```

### Check file size before upload
```bash
ls -lh file.zip  # Check size in human-readable format
emery info       # Check max allowed size
```

### View files on the files branch
```bash
git checkout files
ls -la files/
git checkout main
```

### See upload history
```bash
git log files --oneline
```

### Change file size limit temporarily
Edit `emery_cli/config.py`:
```python
MAX_FILE_SIZE_MB = 500  # Increase to 500 MB
```

Then reinstall:
```bash
pip install -e .
```

## Troubleshooting

### "File too large"
```bash
# Check current max size
emery info

# Edit config if needed
# See "Configuration" section above
```

### "Git error" when uploading
```bash
# Make sure git is configured
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

# Check repository status
git status
```

### "Command not found: emery"
```bash
# Reinstall the CLI
cd Emery
pip install -e .
```

### Unintended files were uploaded
```bash
# Switch to files branch
git checkout files

# See what files are there
ls files/

# Remove unwanted files
rm files/unwanted_file.txt

# Commit the removal
git add files/
git commit -m "Remove unwanted file"
git push

# Return to main
git checkout main
```

## Next Steps

- 📚 Read the full [README.md](README.md)
- 🐛 Report issues on [GitHub](https://github.com/JuanJuanCtrl/Emery/issues)
- 💡 Suggest improvements

---

**Happy uploading! 🎉**
