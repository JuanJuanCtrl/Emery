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

### 1. Upload with File Picker (Recommended)

```bash
emery upload
```

This will:
- ✓ Open native file picker dialog
- ✓ Let you browse and select files/folders
- ✓ Display selected items
- ✓ Copy to the `files/` directory
- ✓ Create/switch to the `files` branch
- ✓ Commit with auto-generated message
- ✓ Push to remote
- ✓ Return to main branch

**In the file picker:**
1. Navigate your file system
2. Select one or multiple files and/or folders
3. Click "Open"
4. Watch as Emery uploads everything

### 2. Upload specific files (command-line)

```bash
emery upload document.pdf report.xlsx
```

Bypasses the file picker and uploads directly.

### 3. Upload a folder (command-line)

```bash
emery upload my_project/
```

All files and subfolders are uploaded with their structure preserved:
```
files/
└── my_project/
    ├── file1.txt
    └── subfolder/
        └── file2.txt
```

### 4. Add a custom commit message

```bash
emery upload -m "Add Q1 2026 financial reports"
```

Then use the file picker to select your files.

Or with command-line paths:

```bash
emery upload -m "Add project files" sales.xlsx my_project/
```

### 5. Copy files without git operations (dry run)

```bash
emery upload --no-commit
```

Opens the file picker, uploads files, but doesn't commit/push.

Later, manually commit if you want:
```bash
cd files/
git add .
git commit -m "Add large files"
git push
```

### 6. View configuration and uploaded files

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

## File Picker Dialog

When you run `emery upload` without arguments, it opens a native file picker:

1. **Run Emery:**
   ```bash
   emery upload
   ```

2. **File picker opens** - Browse your file system

3. **Select files/folders** - Hold Ctrl/Cmd to multi-select

4. **Click Open** - Upload starts automatically

5. **See results** - Terminal shows upload progress and status

### Advantages over terminal drag-and-drop:
- ✓ Native file browser - familiar interface
- ✓ Easy to navigate nested folders
- ✓ Multi-select support
- ✓ Works on all terminals (Windows, macOS, Linux)
- ✓ No terminal window height limitations

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
┌──────────────────┐
│  Open file       │
│  picker dialog   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  User selects    │
│  files/folders   │
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│  Validate    │
│  file size   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Copy files  │
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

### Use the file picker for easy selection
```bash
emery upload
# Navigate, select multiple items (Ctrl/Cmd+Click), and click Open
```

### Quick command-line uploads (skip picker)
```bash
# Upload specific paths directly - bypasses file picker
emery upload /path/to/file.pdf /path/to/folder/
```

### Mix files and folders in one upload
In the file picker:
- Hold Ctrl/Cmd to multi-select
- Select individual files AND entire folders
- All are processed together

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
