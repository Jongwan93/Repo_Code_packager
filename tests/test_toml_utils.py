import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Repo_Code_Packager.toml_utils import load_config

class TestLoadConfig:
    """Tests for load_config function in toml_utils.py"""

    def test_returns_none_when_file_missing(self, tmp_path):
        """Should return None if the config file does not exist"""
        missing_file = tmp_path / "non-existent.toml"
        result = load_config(missing_file)
        assert result is None

    def test_loads_valid_toml_config(self, tmp_path):
        """Should correctly parse a valid TOML file"""
        config_text = """
        output = ""
        tokens = false
        recent = true
        line_numbers = false
        dirs_only = true
        exclude_dirs = ["__pycache__", "venv", ".git"]
        """
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(config_text)

        result = load_config(toml_file)

        assert isinstance(result, dict)
        assert result["output"] == ""
        assert result["tokens"] is False
        assert result["recent"] is True
        assert result["dirs_only"] is True
        assert result["exclude_dirs"] == ["__pycache__", "venv", ".git"]

    def test_invalid_toml_raises_runtime_error(self, tmp_path):
        """Should raise RuntimeError for invalid TOML file"""
        invalid_toml = tmp_path / "bad_config.toml"
        invalid_toml.write_text("invalid_arg")

        with pytest.raises(RuntimeError) as err:
            load_config(invalid_toml)

        assert 'Cannot parse config file' in str(err.value)