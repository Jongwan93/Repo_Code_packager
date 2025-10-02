import tomllib
import os

def load_config(file_path=".repo-code-packager-config.toml"):
    if not os.path.exists(file_path):
        return

    try:
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    except:
        raise RuntimeError(f'Cannot parse config file "{file_path}" as TOML')
    