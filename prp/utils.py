import sys
from pathlib import Path

import prp.config as config
from prp.appdirs import user_cache_dir


def get_virtualenv_path() -> Path:
    unique_name = get_unique_name()
    return Path(
        user_cache_dir('prp'),
        'virtualenvs',
        unique_name
    )


def get_unique_name() -> str:
    name = config.get('name')
    if name is None:
        raise ValueError('The applications name is not defined '
                         'in pyproject.toml [tool.prp]')
    python_version = config.get('python_version')
    if python_version is None:
        python_version = '.'.join([
            sys.version_info.major,
            sys.version_info.major
        ])
    return f'{name}-py{python_version}'
