#!/usr/bin/python3
# coding:utf-8

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from ...utils.compose import compose_file


@add_command("list")
def add_cmd_list(_arg: argp):
    pass


@run_command(add_cmd_list)
def run_cmd_list(cmds: commands) -> int:
    args = cmds.args
    assert isinstance(args.compose_file, compose_file)

    for volume in args.compose_file.volumes:
        cmds.stdout(volume.title)

    return 0


@add_command("volume")
def add_cmd_volume(_arg: argp):
    pass


@run_command(add_cmd_volume, add_cmd_list)
def run_cmd_volume(cmds: commands) -> int:
    return 0
