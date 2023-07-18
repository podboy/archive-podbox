#!/usr/bin/python3
# coding:utf-8

from errno import ENOENT
import os
from typing import Optional
from typing import Sequence

from xarg import DEBUG
from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from ...utils import URL_PROG
from ...utils import __prog__
from ...utils.compose import compose_file
from ...utils.compose import default_project_name
from .backup_service import add_cmd_backup_service
from .service import add_cmd_service
from .systemd import add_cmd_systemd
from .volume import add_cmd_volume


@add_command("compose")
def add_cmd_compose(_arg: argp):
    group = _arg.argument_group("project arguments")
    group.add_argument("-p",
                       "--project-name",
                       type=str,
                       nargs="?",
                       const=None,
                       default=None,
                       metavar="PROJECT_NAME",
                       dest="_project_name_",
                       help="Specify project name (default: directory name)")
    group.add_argument(
        "-f",
        "--file",
        type=str,
        nargs="?",
        const="docker-compose.yml",
        default="docker-compose.yml",
        metavar="FILE",
        dest="_compose_file_",
        help="Specify compose file (default: docker-compose.yml)")


@run_command(add_cmd_compose, add_cmd_systemd, add_cmd_volume, add_cmd_service,
             add_cmd_backup_service)
def run_cmd_compose(cmds: commands) -> int:
    args = cmds.args

    if not os.path.isfile(args._compose_file_):
        return ENOENT

    if args._project_name_ is None:
        args._project_name_ = default_project_name(args._compose_file_)

    args.compose_file = compose_file(args._project_name_, args._compose_file_)
    cmds.args = args
    cmds.log(cmds.args, DEBUG)

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    return cmds.run(root=add_cmd_compose,
                    argv=argv,
                    prog=f"{__prog__}-compose",
                    description="Toolset for podman.",
                    epilog=f"For more, please visit {URL_PROG}")
