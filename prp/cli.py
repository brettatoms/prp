import os
import shlex
import sys
import venv
from argparse import ArgumentParser, Namespace
from subprocess import Popen

from prp import config
from prp import utils


def parse_args(args=None) -> Namespace:
    parser = ArgumentParser("prp", description="Run a command in a virtualenv")
    parser.add_argument(
        "-v", "--venv", nargs="?", const="<print>", help="The virtualenv"
    )
    parser.add_argument("cmd", nargs="+", help="The command to run")

    return parser.parse_args()


def main():
    args = parse_args()
    print(args)
    cmd = args.cmd

    cmd_name = cmd[0]
    alias = config.get_alias(cmd_name)
    if alias is not None:
        cmd = shlex.split(alias) + cmd[1:]

    if args.venv == "<print>":
        venv_path = utils.get_virtualenv_path()
        print(venv_path)
    elif args.venv is not None:
        if os.path.exists(args.venv):
            venv_path = args.venv
        else:
            venv_path = utils.get_virtualenv_path()
    else:
        venv_path = utils.get_virtualenv_path()

    if not venv_path.exists():
        print(f"Creating {venv_path}")
        venv.EnvBuilder(with_pip=True).create(venv_path)

    # Add the virtualenv to PYTHONPATH
    sys.path.insert(0, str(venv_path))

    # Add the virtualenv bin directory to PATH
    os.environ["PATH"] = os.pathsep.join(
        [str(venv_path.joinpath("bin")), os.environ["PATH"]]
    )

    with Popen(cmd, bufsize=0, universal_newlines=True):
        # print to flush buffers and get a new command promp
        print("", end="")


if __name__ == "__main__":
    main()
