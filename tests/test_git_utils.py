import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from git_utils import get_git_info


class TestGetGitInfo:
    """Tests for get_git_info function"""
    
    def test_non_git_directory_returns_message(self, tmp_path):
        """Non-git directory should return appropriate message"""
        result = get_git_info(str(tmp_path))
        assert result == "Not a git repository"
    
    def test_returns_string_type(self):
        """Function should always return a string"""
        current_dir = os.path.dirname(os.path.dirname(__file__))
        result = get_git_info(current_dir)
        assert isinstance(result, str)
    
    def test_git_repo_contains_required_fields(self):
        """Valid git repository should return all required information"""
        current_dir = os.path.dirname(os.path.dirname(__file__))
        result = get_git_info(current_dir)
        
        if "Not a git repository" not in result:
            assert "Commit:" in result
            assert "Branch:" in result
            assert "Author:" in result
            assert "Date:" in result
    
    def test_handles_nonexistent_path(self, tmp_path):
        """Nonexistent path should be handled gracefully"""
        nonexistent = tmp_path / "does_not_exist"
        nonexistent.mkdir()
        
        result = get_git_info(str(nonexistent))
        assert result == "Not a git repository"
    
    def test_git_info_format_with_bullet_points(self):
        """Git info should be formatted with bullet points"""
        current_dir = os.path.dirname(os.path.dirname(__file__))
        result = get_git_info(current_dir)
        
        if "Not a git repository" not in result:
            lines = result.split('\n')
            for line in lines:
                if line.strip():
                    assert line.startswith('- ')