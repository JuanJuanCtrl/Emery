"""Main CLI application for Emery."""

import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

from emery_cli.config import MAX_FILE_SIZE_MB, TARGET_BRANCH, REPO_ROOT, FILES_DIR, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL
from emery_cli.file_handler import FileHandler
from emery_cli.git_handler import GitHandler

app = typer.Typer(
    name="emery",
    help="Upload files to the 'files' branch with drag-and-drop support",
    no_args_is_help=False,
)

console = Console()


def show_banner() -> None:
    """Display application banner."""
    banner = Text("✨ EMERY", justify="center", style="bold cyan")
    console.print(Panel(banner, expand=False, padding=(0, 2)))


def show_info() -> None:
    """Display CLI information."""
    info_text = f"""
[cyan]Max File Size:[/cyan] {MAX_FILE_SIZE_MB} MB
[cyan]Target Branch:[/cyan] {TARGET_BRANCH}
[cyan]Upload Directory:[/cyan] {FILES_DIR}
    """
    console.print(Panel(info_text.strip(), title="Configuration", style="dim"))


@app.command()
def upload(
    files: Optional[List[Path]] = typer.Argument(None, help="Files to upload (drag & drop or specify paths)"),
    auto_commit: bool = typer.Option(True, "--commit/--no-commit", help="Auto-commit and push changes"),
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Custom commit message"),
) -> None:
    """
    Upload files to the repository.
    
    Examples:
        emery upload file1.txt file2.pdf
        emery upload --no-commit file.zip
        emery upload -m "Add new documents" file1.txt file2.txt
    """
    show_banner()
    
    if not files:
        console.print("[yellow]⚠ No files provided[/yellow]")
        show_info()
        return
    
    # Initialize handlers
    file_handler = FileHandler(MAX_FILE_SIZE_MB)
    git_handler = GitHandler(REPO_ROOT)
    
    # Ensure files directory exists
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Process files
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Processing files...", total=len(files))
        
        # Copy files
        file_objects = []
        for file_path_arg in files:
            file_path = Path(file_path_arg).resolve()
            
            if file_path.is_dir():
                console.print(f"[yellow]✓ Skipping directory: {file_path.name}[/yellow]")
                progress.advance(task)
                continue
            
            # Display file info
            file_handler.display_file_info(file_path)
            
            # Copy file
            success, result = file_handler.copy_file(file_path, FILES_DIR)
            if success:
                console.print(f"[green]✓ Uploaded: {file_path.name}[/green]")
                file_objects.append(Path(result))
            else:
                console.print(f"[red]✗ Failed: {result}[/red]")
            
            progress.advance(task)
    
    if not file_objects:
        console.print("[red]✗ No files were successfully uploaded[/red]")
        return
    
    # Git operations
    if auto_commit:
        # Ensure target branch exists
        if not git_handler.ensure_branch(TARGET_BRANCH):
            console.print("[red]✗ Failed to ensure target branch[/red]")
            return
        
        # Save current branch to restore later
        current_branch = git_handler.get_current_branch()
        
        # Switch to target branch
        if not git_handler.switch_branch(TARGET_BRANCH):
            console.print("[red]✗ Failed to switch to target branch[/red]")
            return
        
        try:
            # Stage files - pass absolute paths
            file_paths = [str(f.absolute()) for f in file_objects]
            git_handler.add_files(file_paths)
            
            # Create commit message
            if not message:
                file_names = ", ".join([f.name for f in file_objects])
                message = f"Upload: {file_names}"
            
            # Commit
            git_handler.commit(message, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL)
            
            # Push
            git_handler.push(TARGET_BRANCH)
            
            console.print(f"[green]✓ Successfully uploaded {len(file_objects)} file(s)[/green]")
            
        finally:
            # Try to restore original branch
            try:
                git_handler.switch_branch(current_branch)
            except:
                pass
    else:
        console.print(f"[cyan]✓ Copied {len(file_objects)} file(s) to {FILES_DIR}[/cyan]")
        console.print("[yellow]Use --commit to push to the 'files' branch[/yellow]")


@app.command()
def info() -> None:
    """Display CLI configuration and information."""
    show_banner()
    show_info()
    
    # Show upload directory contents if it exists
    if FILES_DIR.exists():
        uploaded_files = list(FILES_DIR.glob("*"))
        if uploaded_files:
            console.print(f"\n[cyan]Files in {FILES_DIR.name}:[/cyan]")
            for f in uploaded_files:
                if f.is_file():
                    size_mb = f.stat().st_size / (1024 * 1024)
                    console.print(f"  • {f.name} ({size_mb:.2f} MB)")


@app.command()
def clean() -> None:
    """Clear all uploaded files from the files directory."""
    if not FILES_DIR.exists():
        console.print("[yellow]✓ Files directory is already empty[/yellow]")
        return
    
    import shutil
    
    try:
        shutil.rmtree(FILES_DIR)
        console.print("[green]✓ Cleared files directory[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error clearing directory: {e}[/red]")


def main() -> None:
    """Main entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]✓ Cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
