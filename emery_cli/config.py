"""Configuration for Emery CLI."""

import os
from pathlib import Path

# Max file size in MB
MAX_FILE_SIZE_MB = 100

# Target branch for uploads
TARGET_BRANCH = "files"

# Repository root
REPO_ROOT = Path(__file__).parent.parent

# Files upload directory
FILES_DIR = REPO_ROOT / "files"

# Git config
GIT_AUTHOR_NAME = os.getenv("GIT_AUTHOR_NAME", "Emery CLI")
GIT_AUTHOR_EMAIL = os.getenv("GIT_AUTHOR_EMAIL", "cli@emery.local")
