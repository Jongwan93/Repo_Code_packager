import pytest
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_packager import (
    generate_summary,
    format_json,
    format_markdown,
    create_structure_tree
)


class TestGenerateSummary:
    """Tests for generate_summary function"""
    
    def test_summary_with_multiple_files(self):
        """Summary should correctly count files and lines"""
        file_list = ["file1.py", "file2.py", "file3.txt"]
        total_lines = 150
        
        result = generate_summary(file_list, total_lines)
        
        assert "Total files: 3" in result
        assert "Total lines: 150" in result
    
    def test_summary_with_single_file(self):
        """Summary should work with a single file"""
        file_list = ["single.py"]
        total_lines = 42
        
        result = generate_summary(file_list, total_lines)
        
        assert "Total files: 1" in result
        assert "Total lines: 42" in result
    
    def test_summary_with_no_files(self):
        """Summary should handle empty file list"""
        file_list = []
        total_lines = 0
        
        result = generate_summary(file_list, total_lines)
        
        assert "Total files: 0" in result
        assert "Total lines: 0" in result
        assert 1 == 2 # intentionally added this line for Lab 8
    
    def test_summary_format(self):
        """Summary should follow expected format"""
        file_list = ["test.py"]
        total_lines = 10
        
        result = generate_summary(file_list, total_lines)
        lines = result.split('\n')
        
        # Should have exactly 2 lines
        assert len(lines) == 2
        assert lines[0].startswith("- Total files:")
        assert lines[1].startswith("- Total lines:")


class TestFormatJson:
    """Tests for format_json function"""
    
    def test_converts_dict_to_json_string(self):
        """Dictionary should be converted to JSON string"""
        data = {"name": "test", "value": 123}
        
        result = format_json(data)
        
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == data
    
    def test_json_output_is_indented(self):
        """JSON output should be properly indented"""
        data = {"key": "value", "nested": {"inner": "data"}}
        
        result = format_json(data)
        
        # Should contain newlines and spaces for indentation
        assert "\n" in result
        assert "  " in result
    
    def test_handles_empty_dict(self):
        """Empty dictionary should produce valid JSON"""
        data = {}
        
        result = format_json(data)
        
        assert result == "{}"
    
    def test_preserves_data_types(self):
        """Different data types should be preserved"""
        data = {
            "string": "text",
            "number": 42,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "object": {"nested": "value"}
        }
        
        result = format_json(data)
        parsed = json.loads(result)
        
        assert parsed["string"] == "text"
        assert parsed["number"] == 42
        assert parsed["boolean"] == True
        assert parsed["null"] is None
        assert parsed["array"] == [1, 2, 3]
        assert parsed["object"]["nested"] == "value"


class TestFormatMarkdown:
    """Tests for format_markdown function"""
    
    def test_creates_complete_markdown_document(self):
        """Markdown output should have all required sections"""
        data = {
            "base_path": "/test/path",
            "git_info": "Branch: main",
            "structure_tree": "├── file1.py",
            "file_contents": "### File: test.py",
            "summary": "Total files: 1"
        }
        
        result = format_markdown(data)
        
        assert "# Repository Context" in result
        assert "## File System Location" in result
        assert "## Git Info" in result
        assert "## Structure" in result
        assert "## File Contents" in result
        assert "## Summary" in result
    
    def test_includes_all_data_values(self):
        """All provided data should appear in markdown output"""
        data = {
            "base_path": "/unique/path/123",
            "git_info": "Commit: abc123",
            "structure_tree": "test_tree_content",
            "file_contents": "test_file_content",
            "summary": "test_summary_content"
        }
        
        result = format_markdown(data)
        
        assert "/unique/path/123" in result
        assert "Commit: abc123" in result
        assert "test_tree_content" in result
        assert "test_file_content" in result
        assert "test_summary_content" in result
    
    def test_sections_appear_in_correct_order(self):
        """Sections should appear in the expected order"""
        data = {
            "base_path": "path",
            "git_info": "git",
            "structure_tree": "tree",
            "file_contents": "contents",
            "summary": "summary"
        }
        
        result = format_markdown(data)
        
        location_pos = result.find("File System Location")
        git_pos = result.find("Git Info")
        structure_pos = result.find("Structure")
        contents_pos = result.find("File Contents")
        summary_pos = result.find("Summary")
        
        assert location_pos < git_pos < structure_pos < contents_pos < summary_pos


class TestCreateStructureTree:
    """Tests for create_structure_tree function"""
    
    def test_single_file_in_tree(self, tmp_path):
        """Tree should display a single file correctly"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        result = create_structure_tree([str(test_file)], str(tmp_path))
        
        assert "test.txt" in result
    
    def test_nested_directory_structure(self, tmp_path):
        """Tree should show nested directory structure"""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        
        file1 = tmp_path / "root.txt"
        file2 = subdir / "nested.txt"
        file1.write_text("content1")
        file2.write_text("content2")
        
        result = create_structure_tree([str(file1), str(file2)], str(tmp_path))
        
        assert "root.txt" in result
        assert "subdir" in result
        assert "nested.txt" in result
    
    def test_empty_file_list(self, tmp_path):
        """Empty file list should produce empty tree"""
        result = create_structure_tree([], str(tmp_path))
        assert result == ""
    
    def test_multiple_files_in_same_directory(self, tmp_path):
        """Multiple files in same directory should all appear"""
        files = []
        for i in range(3):
            f = tmp_path / f"file{i}.txt"
            f.write_text(f"content{i}")
            files.append(str(f))
        
        result = create_structure_tree(files, str(tmp_path))
        
        for i in range(3):
            assert f"file{i}.txt" in result
    
    def test_deeply_nested_structure(self, tmp_path):
        """Deeply nested directories should be represented correctly"""
        deep_dir = tmp_path / "level1" / "level2" / "level3"
        deep_dir.mkdir(parents=True)
        
        deep_file = deep_dir / "deep.txt"
        deep_file.write_text("deep content")
        
        result = create_structure_tree([str(deep_file)], str(tmp_path))
        
        assert "level1" in result
        assert "level2" in result
        assert "level3" in result
        assert "deep.txt" in result