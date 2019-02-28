import os
import subprocess
import sys
import venv
from pathlib import Path
from binascii import crc32

import prp.config as config
from prp.appdirs import user_cache_dir


def get_cached_depdencies_hash_path() -> Path:
    return Path(
        user_cache_dir('prp'),
        "dependencies_hash",
        get_unique_name()
    )


def get_virtualenv_path() -> Path:
    unique_name = get_unique_name()
    return Path(
        user_cache_dir('prp'),
        'virtualenvs',
        unique_name
    )


def dependencies_needs_updating() -> bool:
    deps_filename = config.get(
        'requirements_filename', 'requirements.txt'
    )
    deps_path = Path(Path.cwd(), deps_filename)
    with open(deps_path, 'rb') as f:
        contents = f.read()
        current_deps_crc32 = crc32(contents)

    cached_path = get_cached_depdencies_hash_path()
    cached_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cached_path) as f:
        return f.read() !=  str(current_deps_crc32)


def update_dependencies_hash():
    deps_filename = config.get(
        'requirements_filename', 'requirements.txt'
    )
    deps_path = Path(Path.cwd(), deps_filename)
    with open(deps_path, 'rb') as f:
        contents = f.read()
        current_deps_crc32 = crc32(contents)

    cache_dependencies_hash_path = Path(
        user_cache_dir('prp'),
        "dependencies_hash",
        get_unique_name()
    )

    cached_path = get_cached_depdencies_hash_path()
    cached_path.parent.mkdir(parents=True, exist_ok=True)
    print(f'Updating dependencies hash in {cached_path}...')
    print(current_deps_crc32)
    with open(cached_path, 'w') as f:
        f.write(str(current_deps_crc32))


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


def main():
    # TODO: pipenv uses app-name-{hash} where poetry uses a name based on the
    # app name and version...seems like the poetry version could have conflicts
    # if you're running the same thing at different paths
    virtualenv_path = get_virtualenv_path()

    # if it doesn't exist then run pip install requirements.txt
    # if it doesn't exist then run pip install requirements.txt
    if not virtualenv_path.exists():
        # create virtualenv
        print(f'Creating {virtualenv_path}')
        virtualenv_path.mkdir(parents=True)

    if dependencies_needs_updating():
        builder = venv.EnvBuilder(upgrade=True, with_pip=True)
        builder.create(virtualenv_path)


        deps_filename = config.get(
            'requirements_filename', 'requirements.txt'
        )
        subprocess.run(['pip', 'install', '-U', '-r', deps_filename])
        update_dependencies_hash()

    # Add the virtualenv to PYTHONPATH
    sys.path.insert(0, str(virtualenv_path))

    # Add the virtualenv bin directory to PATH
    os.environ['PATH'] = os.pathsep.join([
        str(virtualenv_path.joinpath('bin')),
        os.environ['PATH']
    ])

    # Run the command
    subprocess.run(sys.argv[2:])


if __name__ == '__main__':
    main()
