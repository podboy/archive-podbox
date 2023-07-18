#!/usr/bin/python3
# coding:utf-8

from typing import Optional
from typing import Sequence

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from ..utils import URL_PROG
from ..utils import __prog__
from ..utils import __version__
from .compose import add_cmd_compose


@add_command(__prog__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_compose)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = f"{__prog__} {__version__}"
    return cmds.run(root=add_cmd,
                    argv=argv,
                    prog=__prog__,
                    description="Toolset for podman.",
                    epilog=f"For more, please visit {URL_PROG}")
