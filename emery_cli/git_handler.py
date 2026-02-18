"""Git operations for Emery CLI."""

from pathlib import Path
from git import Repo
from rich.console import Console
from typing import Optional

console = Console()

class GitHandler:
    """Handle git operations for file uploads."""

    def __init__(self, repo_path: Path):
        """Initialize git handler with repository path.
        
        Args:
            repo_path: Path to the git repository
        """
        self.repo = Repo(str(repo_path))
        self.repo_path = repo_path

    def ensure_branch(self, branch_name: str) -> bool:
        """Ensure the target branch exists.
        
        Args:
            branch_name: Name of the branch to ensure
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if branch exists
            if branch_name not in [ref.name for ref in self.repo.heads]:
                # Create new branch
                console.print(f"[cyan]Creating branch '{branch_name}'...[/cyan]")
                self.repo.create_head(branch_name)
            
            return True
        except Exception as e:
            console.print(f"[red]Error ensuring branch: {e}[/red]")
            return False

    def switch_branch(self, branch_name: str) -> bool:
        """Switch to target branch.
        
        Args:
            branch_name: Name of the branch to switch to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.repo.heads[branch_name].checkout()
            console.print(f"[green]✓ Switched to branch '{branch_name}'[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error switching branch: {e}[/red]")
            return False

    def add_files(self, file_paths: list) -> bool:
        """Stage files for commit.
        
        Args:
            file_paths: List of file paths to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            rel_paths = []
            for file_path in file_paths:
                # Convert to Path object and make absolute
                abs_path = Path(file_path).resolve()
                # Make path relative to repo root
                rel_path = abs_path.relative_to(self.repo_path)
                rel_paths.append(str(rel_path))
            
            if rel_paths:
                self.repo.index.add(rel_paths)
            return True
        except Exception as e:
            console.print(f"[red]Error staging files: {e}[/red]")
            return False

    def commit(self, message: str, author_name: str, author_email: str) -> bool:
        """Commit staged files.
        
        Args:
            message: Commit message
            author_name: Name of the author
            author_email: Email of the author
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from git.util import Actor
            
            if not self.repo.index.diff("HEAD"):
                console.print("[yellow]✓ No changes to commit[/yellow]")
                return True
            
            actor = Actor(author_name, author_email)
            self.repo.index.commit(message, author=actor, committer=actor)
            console.print(f"[green]✓ Committed: {message}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error committing: {e}[/red]")
            return False

    def push(self, branch_name: str) -> bool:
        """Push changes to remote.
        
        Args:
            branch_name: Name of the branch to push
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.repo.remotes:
                console.print("[yellow]⚠ No remote configured[/yellow]")
                return True
            
            origin = self.repo.remotes.origin
            origin.pull(branch_name)
            origin.push(branch_name)
            console.print(f"[green]✓ Pushed to origin/{branch_name}[/green]")
            return True
        except Exception as e:
            console.print(f"[yellow]⚠ Push skipped: {e}[/yellow]")
            return True  # Don't fail if push fails (might not have remote)

    def get_current_branch(self) -> str:
        """Get the current branch name.
        
        Returns:
            Current branch name
        """
        return self.repo.active_branch.name
