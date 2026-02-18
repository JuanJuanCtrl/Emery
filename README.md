# ✨ Emery

A modern, minimal Python CLI for uploading files with drag-and-drop support. All files are automatically organized and pushed to the `files` branch of your repository.

## Features

- 🎯 **Drag & Drop Support** - Simply drag files into the terminal
- 📁 **Smart File Organization** - Automatic duplicate handling
- 📊 **File Size Management** - Configurable max file size (default 100MB)
- 🔀 **Git Integration** - Auto-commit and push to the `files` branch
- 🎨 **Modern CLI** - Beautiful terminal UI with Rich
- ⚡ **Minimal & Fast** - Lightweight with zero bloat

## Installation

### From Source

```bash
git clone https://github.com/JuanJuanCtrl/Emery.git
cd Emery
pip install -e .
```

### From PyPI (coming soon)

```bash
pip install emery-cli
```

## Quick Start

### Upload files

```bash
# Simple upload
emery upload file1.txt file2.pdf

# With custom commit message
emery upload -m "Add project documents" file1.txt file2.txt

# Without auto-commit
emery upload --no-commit file.zip
```

### Drag and Drop

Most terminals support dragging files:

```bash
emery upload <drag files here>
```

### View information

```bash
# Show configuration and uploaded files
emery info

# Clear uploaded files
emery clean
```

## Configuration

Customize behavior by setting environment variables:

```bash
# Set git author info
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your@email.com"
```

## Configuration File

Edit `emery_cli/config.py` to customize:

```python
MAX_FILE_SIZE_MB = 100  # Maximum file size in MB
TARGET_BRANCH = "files"  # Target git branch
FILES_DIR = REPO_ROOT / "files"  # Upload directory
```

## Project Structure

```
Emery/
├── emery_cli/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration settings
│   ├── file_handler.py       # File operations & validation
│   ├── git_handler.py        # Git operations
│   └── main.py              # CLI application & commands
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata & build config
├── README.md               # This file
└── LICENSE                 # MIT License
```

## Usage Examples

### Upload and auto-commit

```bash
emery upload document.pdf
```

This will:
1. Validate the file (check size, existence)
2. Display file information
3. Copy to the `files/` directory
4. Create and commit to the `files` branch
5. Push changes to remote

### Upload multiple files with message

```bash
emery upload -m "Add Q1 reports" sales.xlsx expenses.xlsx revenue.pdf
```

### Copy files without git operations

```bash
emery upload --no-commit large_file.zip
```

### View configuration and uploaded files

```bash
emery info
```

### Clear uploaded files

```bash
emery clean
```

## Requirements

- Python 3.8+
- Git
- Terminal with drag-and-drop support (most modern terminals)

## Dependencies

- **Typer** - Modern CLI framework
- **Rich** - Beautiful terminal output
- **GitPython** - Git operations
- **Click** - CLI utilities

## Workflow

1. Run `emery upload <files>`
2. CLI validates file sizes
3. Files are copied to the `files/` directory
4. Changes are staged and committed to the `files` branch
5. Changes are pushed to the remote repository

## Tips

- **Drag & Drop**: Most terminals (iTerm2, Terminal.app, Windows Terminal, VSCode, etc.) support dragging files
- **Batch Upload**: Upload multiple files at once for efficiency
- **Custom Messages**: Use `-m` to add meaningful commit messages
- **Dry Run**: Use `--no-commit` to test uploads without git operations

## Troubleshooting

### Files not uploading

Check file size and configuration:
```bash
emery info
```

The maximum file size is shown in the configuration panel.

### Git errors

Ensure you have:
- Git configured: `git config --global user.email "you@example.com"`
- Repository initialized: `git init` (usually already done)
- Remote configured (optional): `git remote add origin <url>`

## License

MIT - See [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.

---

Made with ❤️ for developers
