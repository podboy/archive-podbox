#!/usr/bin/python3
# coding:utf-8

from typing import Optional
from typing import Sequence

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from ...utils import URL_PROG
from ...utils import __prog__


@add_command("enable")
def add_cmd_enable(_arg: argp):
    pass


@run_command(add_cmd_enable)
def run_cmd_enable(cmds: commands) -> int:
    return 0


@add_command("disable")
def add_cmd_disable(_arg: argp):
    pass


@run_command(add_cmd_disable)
def run_cmd_disable(cmds: commands) -> int:
    return 0


@add_command("systemd")
def add_cmd_systemd(_arg: argp):
    pass


@run_command(add_cmd_systemd, add_cmd_enable, add_cmd_disable)
def run_cmd_systemd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    return cmds.run(root=add_cmd_systemd,
                    argv=argv,
                    prog=f"{__prog__}-compose-systemd",
                    description="Toolset for podman.",
                    epilog=f"For more, please visit {URL_PROG}")
