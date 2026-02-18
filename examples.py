"""Example script showing how to use Emery CLI programmatically."""

from pathlib import Path
from emery_cli.file_handler import FileHandler
from emery_cli.git_handler import GitHandler
from emery_cli.config import MAX_FILE_SIZE_MB, TARGET_BRANCH, REPO_ROOT, FILES_DIR, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL


def example_basic_upload():
    """Example: Basic file upload without git."""
    file_handler = FileHandler(MAX_FILE_SIZE_MB)
    
    # Validate a file
    test_file = Path("example.txt")
    is_valid, message = file_handler.validate_file(test_file)
    
    if is_valid:
        # Copy file
        success, result = file_handler.copy_file(test_file, FILES_DIR)
        if success:
            print(f"✓ File copied to: {result}")
        else:
            print(f"✗ Error: {result}")


def example_with_git():
    """Example: Upload with git commit."""
    file_handler = FileHandler(MAX_FILE_SIZE_MB)
    git_handler = GitHandler(REPO_ROOT)
    
    # Prepare files
    test_files = [Path("file1.txt"), Path("file2.txt")]
    
    # Copy files
    successful, errors = file_handler.copy_files_batch(test_files, FILES_DIR)
    
    if successful:
        # Ensure branch exists
        git_handler.ensure_branch(TARGET_BRANCH)
        
        # Switch to target branch
        git_handler.switch_branch(TARGET_BRANCH)
        
        # Stage and commit
        file_paths = [str(f.absolute()) for f in successful]
        git_handler.add_files(file_paths)
        git_handler.commit("Upload files", GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL)
        
        # Push to remote
        git_handler.push(TARGET_BRANCH)
        
        print(f"✓ Successfully uploaded {len(successful)} file(s)")
    
    if errors:
        print(f"✗ Errors: {errors}")


if __name__ == "__main__":
    print("See QUICKSTART.md for command-line usage examples")
    print("\nFor programmatic usage:")
    print("  - Import FileHandler and GitHandler")
    print("  - Check emery_cli/config.py for settings")
