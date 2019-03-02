from functools import lru_cache
from pathlib import Path
import toml


@lru_cache()
def _load_pyproject_toml():
    pyproject_path = Path(Path.cwd(), "pyproject.toml")
    with open(pyproject_path, 'r') as f:
        d = toml.load(f)
        return d.get('tool', {}).get('prp', {})


def get(key, default=None):
    config = _load_pyproject_toml()
    return config.get(key, default)


def get_alias(name):
    d = _load_pyproject_toml()
    return d.get('aliases', {}).get(name, None)
