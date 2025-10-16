from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional
import re


class GitHubService:
    """Service for handling GitHub repository operations"""
    
    @staticmethod
    def validate_github_url(url: str) -> bool:
        """Validate GitHub URL format"""
        github_pattern = r'^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?$'
        return bool(re.match(github_pattern, url))
    
    @staticmethod
    def clone_repository(github_url: str) -> str:
        """Clone GitHub repository to temporary directory"""
        if not GitHubService.validate_github_url(github_url):
            raise ValueError(f"Invalid GitHub URL: {github_url}")
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="doubletrust_github_")
        
        try:
            # Clone the repository
            result = subprocess.run(
                ["git", "clone", github_url, temp_dir],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Failed to clone repository: {result.stderr}")
            
            return temp_dir
            
        except subprocess.TimeoutExpired:
            # Clean up on timeout
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError("Repository clone timed out")
        except Exception as e:
            # Clean up on any error
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to clone repository: {str(e)}")
    
    @staticmethod
    def cleanup_temp_directory(path: str) -> None:
        """Clean up temporary directory"""
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
        except Exception as e:
            # Log error but don't raise to avoid masking other errors
            print(f"Warning: Failed to cleanup temp directory {path}: {e}")
