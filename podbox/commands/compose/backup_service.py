#!/usr/bin/python3
# coding:utf-8

from xarg import DEBUG
from xarg import INFO
from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from ...utils.compose import compose_file
from ...utils.compose import compose_service


@add_command("backup-service")
def add_cmd_backup_service(_arg: argp):
    _arg.add_opt_on("-y", "--yes", dest="_backup_yes_", help="Force update")
    group = _arg.argument_group("service arguments")
    group.add_argument("-s",
                       "--services",
                       type=str,
                       nargs="+",
                       metavar="SERVICE_NAME",
                       dest="_backup_services_",
                       help="Specify backup services, default: all services")
    group.add_argument("--service-name",
                       type=str,
                       nargs="?",
                       const="backup",
                       default="backup",
                       metavar="SERVICE_NAME",
                       dest="_backup_service_name_",
                       help="Specify backup service name, default: backup")
    group.add_argument(
        "--container-name",
        type=str,
        nargs="?",
        const=None,
        default=None,
        metavar="CONTAINER_NAME",
        dest="_backup_container_name_",
        help="Specify backup service container name, default: backup")


@run_command(add_cmd_backup_service)
def run_cmd_backup_service(cmds: commands) -> int:
    args = cmds.args
    assert isinstance(args.compose_file, compose_file)

    backup_services = None if args._backup_services_ is None else [
        i.lower() for i in args._backup_services_
    ]
    backup_service_name = args._backup_service_name_

    backup_volumes = []
    for service in args.compose_file.services:
        service_name = service.title.lower()
        if backup_services is not None and service_name not in backup_services:
            cmds.log(f"ignore service: {service.title}", DEBUG)
            continue
        if service_name == backup_service_name:
            # TODO: check update
            continue
        cmds.log(f"backup service: {service.title}", INFO)
        for volume in service.volumes:
            if volume.type != "volume":
                continue
            volume_source = volume.source
            cmds.log(f"\tvolume {volume_source}", INFO)
            if volume_source not in backup_volumes:
                backup_volumes.append(volume_source)
    cmds.log(f"backup volumes: {backup_volumes}", INFO)

    backup_service = args.compose_file.services[backup_service_name]
    if isinstance(backup_service, compose_service):
        backup_service_value = backup_service.value
        cmds.log(f"update: {backup_service_value}", DEBUG)

    return 0
