"""File operations for Emery CLI."""

import shutil
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

class FileHandler:
    """Handle file operations for uploads."""

    def __init__(self, max_size_mb: int = 100):
        """Initialize file handler.
        
        Args:
            max_size_mb: Maximum file size in MB
        """
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_size_mb = max_size_mb

    def validate_file(self, file_path: Path) -> tuple[bool, str]:
        """Validate if file can be uploaded.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not file_path.exists():
            return False, f"File not found: {file_path}"
        
        if not file_path.is_file():
            return False, f"Path is not a file: {file_path}"
        
        file_size = file_path.stat().st_size
        
        if file_size > self.max_size_bytes:
            size_mb = file_size / (1024 * 1024)
            return False, f"File too large: {size_mb:.2f}MB (max: {self.max_size_mb}MB)"
        
        return True, "Valid"

    def copy_file(self, source_path: Path, dest_dir: Path) -> tuple[bool, str]:
        """Copy file to destination directory.
        
        Args:
            source_path: Source file path
            dest_dir: Destination directory path
            
        Returns:
            Tuple of (success, message)
        """
        is_valid, message = self.validate_file(source_path)
        if not is_valid:
            return False, message
        
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / source_path.name
            
            # Handle duplicate filenames
            if dest_path.exists():
                name = source_path.stem
                ext = source_path.suffix
                counter = 1
                while dest_path.exists():
                    dest_path = dest_dir / f"{name}_{counter}{ext}"
                    counter += 1
            
            shutil.copy2(source_path, dest_path)
            return True, str(dest_path)
        except Exception as e:
            return False, f"Error copying file: {e}"

    def validate_directory(self, dir_path: Path) -> tuple[bool, str]:
        """Validate if directory can be uploaded.
        
        Args:
            dir_path: Path to the directory
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not dir_path.exists():
            return False, f"Directory not found: {dir_path}"
        
        if not dir_path.is_dir():
            return False, f"Path is not a directory: {dir_path}"
        
        # Get all files in directory (recursively)
        files = list(dir_path.rglob("*"))
        file_count = sum(1 for f in files if f.is_file())
        
        if file_count == 0:
            return False, f"Directory is empty: {dir_path}"
        
        # Check if any file exceeds size limit
        oversized_files = []
        for file_path in files:
            if file_path.is_file():
                file_size = file_path.stat().st_size
                if file_size > self.max_size_bytes:
                    size_mb = file_size / (1024 * 1024)
                    oversized_files.append(f"{file_path.name} ({size_mb:.2f}MB)")
        
        if oversized_files:
            return False, f"Files too large: {', '.join(oversized_files[:3])}{'...' if len(oversized_files) > 3 else ''}"
        
        return True, f"Valid ({file_count} files)"

    def copy_directory(self, source_dir: Path, dest_parent: Path) -> tuple[bool, str, List[Path]]:
        """Copy directory recursively to destination.
        
        Args:
            source_dir: Source directory path
            dest_parent: Parent destination directory path
            
        Returns:
            Tuple of (success, message, list_of_copied_files)
        """
        is_valid, message = self.validate_directory(source_dir)
        if not is_valid:
            return False, message, []
        
        try:
            # Create destination with source directory name
            dest_dir = dest_parent / source_dir.name
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            copied_files = []
            
            # Recursively copy all files
            for source_file in source_dir.rglob("*"):
                if source_file.is_file():
                    # Get relative path to preserve structure
                    rel_path = source_file.relative_to(source_dir)
                    dest_file = dest_dir / rel_path
                    
                    # Create parent directories if needed
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(source_file, dest_file)
                    copied_files.append(dest_file)
            
            return True, str(dest_dir), copied_files
        except Exception as e:
            return False, f"Error copying directory: {e}", []

    def copy_files_batch(self, source_paths: List[Path], dest_dir: Path) -> tuple[List[Path], List[str]]:
        """Copy multiple files to destination directory.
        
        Args:
            source_paths: List of source file paths
            dest_dir: Destination directory path
            
        Returns:
            Tuple of (successful_paths, error_messages)
        """
        successful = []
        errors = []
        
        for path in source_paths:
            success, result = self.copy_file(path, dest_dir)
            if success:
                successful.append(Path(result))
            else:
                errors.append(f"{path.name}: {result}")
        
        return successful, errors

    def get_file_info(self, file_path: Path) -> dict:
        """Get file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        stat = file_path.stat()
        return {
            "name": file_path.name,
            "size_bytes": stat.st_size,
            "size_mb": stat.st_size / (1024 * 1024),
            "modified": datetime.fromtimestamp(stat.st_mtime),
        }

    def display_file_info(self, file_path: Path) -> None:
        """Display formatted file information.
        
        Args:
            file_path: Path to the file
        """
        info = self.get_file_info(file_path)
        
        table = Table(title="File Information", show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Name", info["name"])
        table.add_row("Size", f"{info['size_mb']:.2f} MB ({info['size_bytes']:,} bytes)")
        table.add_row("Max Allowed", f"{self.max_size_mb} MB")
        table.add_row("Modified", info["modified"].strftime("%Y-%m-%d %H:%M:%S"))
        
        console.print(table)
