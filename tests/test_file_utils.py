import pytest
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_utils import get_all_files, is_recently_modified


class TestIsRecentlyModified:
    """Tests for is_recently_modified function"""
    
    def test_nonexistent_file_returns_false(self):
        """Non-existent file should return False"""
        result = is_recently_modified("nonexistent_file.txt")
        assert result == False
    
    def test_recently_created_file_returns_true(self, tmp_path):
        """Recently created file should return True"""
        test_file = tmp_path / "recent.txt"
        test_file.write_text("test content")
        
        result = is_recently_modified(str(test_file), days=7)
        assert result == True
    
    def test_file_modified_beyond_time_window(self, tmp_path):
        """File modified beyond the time window should return False"""
        test_file = tmp_path / "old.txt"
        test_file.write_text("old content")
        
        # Set modification time to 10 days ago
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(str(test_file), (ten_days_ago, ten_days_ago))
        
        # Check with 7 day window
        result = is_recently_modified(str(test_file), days=7)
        assert result == False
    
    def test_file_exactly_at_boundary(self, tmp_path):
        """File at exact boundary of time window"""
        test_file = tmp_path / "boundary.txt"
        test_file.write_text("content")
        
        # Set to exactly 7 days ago
        seven_days_ago = time.time() - (7 * 86400) + 1
        os.utime(str(test_file), (seven_days_ago, seven_days_ago))
        
        result = is_recently_modified(str(test_file), days=7)
        # Should return True since it's within the window (<=)
        assert result == True


class TestGetAllFiles:
    """Tests for get_all_files function"""
    
    def test_single_file_path(self, tmp_path):
        """Single file path should return that file"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        result = get_all_files([str(test_file)])
        
        assert len(result) == 1
        assert str(test_file) in result
    
    def test_directory_returns_all_files(self, tmp_path):
        """Directory path should return all files inside"""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.py"
        file1.write_text("content1")
        file2.write_text("content2")
        
        result = get_all_files([str(tmp_path)])
        
        assert len(result) == 2
        assert str(file1) in result
        assert str(file2) in result
    
    def test_hidden_files_are_excluded(self, tmp_path):
        """Files starting with . should be excluded"""
        visible = tmp_path / "visible.txt"
        hidden = tmp_path / ".hidden.txt"
        visible.write_text("visible")
        hidden.write_text("hidden")
        
        result = get_all_files([str(tmp_path)])
        
        assert len(result) == 1
        assert str(visible) in result
        assert str(hidden) not in result
    
    def test_hidden_directories_are_excluded(self, tmp_path):
        """Directories starting with . should be excluded"""
        visible_dir = tmp_path / "visible"
        hidden_dir = tmp_path / ".hidden"
        visible_dir.mkdir()
        hidden_dir.mkdir()
        
        visible_file = visible_dir / "file.txt"
        hidden_file = hidden_dir / "file.txt"
        visible_file.write_text("visible")
        hidden_file.write_text("hidden")
        
        result = get_all_files([str(tmp_path)])
        
        assert len(result) == 1
        assert str(visible_file) in result
        assert str(hidden_file) not in result
    
    def test_exclude_dirs_parameter(self, tmp_path):
        """Specified directories should be excluded"""
        (tmp_path / "include").mkdir()
        (tmp_path / "exclude").mkdir()
        
        file1 = tmp_path / "include" / "file1.txt"
        file2 = tmp_path / "exclude" / "file2.txt"
        file1.write_text("include me")
        file2.write_text("exclude me")
        
        result = get_all_files([str(tmp_path)], exclude_dirs=["exclude"])
        
        assert len(result) == 1
        assert str(file1) in result
        assert str(file2) not in result
    
    def test_multiple_exclude_directories(self, tmp_path):
        """Multiple directories can be excluded at once"""
        (tmp_path / "keep").mkdir()
        (tmp_path / "skip1").mkdir()
        (tmp_path / "skip2").mkdir()
        
        keep_file = tmp_path / "keep" / "file.txt"
        skip_file1 = tmp_path / "skip1" / "file.txt"
        skip_file2 = tmp_path / "skip2" / "file.txt"
        
        keep_file.write_text("keep")
        skip_file1.write_text("skip1")
        skip_file2.write_text("skip2")
        
        result = get_all_files([str(tmp_path)], exclude_dirs=["skip1", "skip2"])
        
        assert len(result) == 1
        assert str(keep_file) in result
    
    def test_empty_path_list(self):
        """Empty path list should return empty result"""
        result = get_all_files([])
        assert result == []
    
    def test_returns_absolute_paths(self, tmp_path):
        """Function should return absolute paths"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        result = get_all_files([str(test_file)])
        
        assert len(result) == 1
        assert os.path.isabs(result[0])
    
    def test_nested_directory_structure(self, tmp_path):
        """Files in nested directories should be found"""
        subdir = tmp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)
        
        file1 = tmp_path / "root.txt"
        file2 = tmp_path / "subdir" / "mid.txt"
        file3 = subdir / "deep.txt"
        
        file1.write_text("root")
        file2.write_text("mid")
        file3.write_text("deep")
        
        result = get_all_files([str(tmp_path)])
        
        assert len(result) == 3
        assert str(file1) in result
        assert str(file2) in result
        assert str(file3) in result
    
    def test_multiple_path_arguments(self, tmp_path):
        """Multiple paths can be provided as arguments"""
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()
        
        file1 = dir1 / "file1.txt"
        file2 = dir2 / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")
        
        result = get_all_files([str(dir1), str(dir2)])
        
        assert len(result) == 2
        assert str(file1) in result
        assert str(file2) in result