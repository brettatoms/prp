import os
import subprocess
import sys

import click

from prp import config
from prp import utils


@click.group()
def cli():
    pass


@cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('command', nargs=-1, type=click.UNPROCESSED, required=True)
def run(command):
    """Run a command or alias."""

    # TODO: pipenv uses app-name-{hash} where poetry uses a name based on the
    # app name and version...seems like the poetry version could have conflicts
    # if you're running the same thing at different paths
    virtualenv_path = utils.get_virtualenv_path()

    # if it doesn't exist then run pip install requirements.txt
    # if it doesn't exist then run pip install requirements.txt
    if not virtualenv_path.exists():
        # create virtualenv
        print(f'Creating {virtualenv_path}')
        virtualenv_path.mkdir(parents=True)

    # Add the virtualenv to PYTHONPATH
    sys.path.insert(0, str(virtualenv_path))

    # Add the virtualenv bin directory to PATH
    os.environ['PATH'] = os.pathsep.join([
        str(virtualenv_path.joinpath('bin')),
        os.environ['PATH']
    ])

    # Run the command
    command_name = command[0]
    alias = config.get_alias(command_name)
    if alias is not None:
        command = alias + ' '.join(command[1:])
    subprocess.run(command, shell=True)


def main():
    cli(prog_name='prp')


if __name__ == '__main__':
    main()
