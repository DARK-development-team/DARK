import os
import subprocess

from .common import data_path, preserve_cwd
import shutil
import venv
from .platform_utils import *


def tournaments_data_path():
    return 'tournaments'


def tround_tournaments_path(name, tournament):
    return f'{tournament.name}/{name}'


def full_tround_path(name, tournament):
    return f'{data_path()}/{tournaments_data_path()}/{tround_tournaments_path(name, tournament)}'


@preserve_cwd()
def create_tround(name, tournament, platform):
    shutil.copytree(full_platform_path(platform), full_tround_path(name, tournament))


class EnvBuilder(venv.EnvBuilder):
    def __init__(self, *args, **kwargs):
        self.context = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        self.context = context


def create_venv(path):
    venv_builder = EnvBuilder(with_pip=True)
    venv_builder.create(f'{os.getcwd()}/{path}/venv')
    return venv_builder.context


def install_dependencies(venv_context, requirements_path):
    command = [venv_context.env_exe] + ['-m', 'pip', 'install', '-r', requirements_path]
    return subprocess.check_call(command)


@preserve_cwd()
def prepare_tround_venv(name, tournament):
    context = create_venv(full_tround_path(name, tournament))
    install_dependencies(context, f'{full_tround_path(name, tournament)}/requirements.txt')


@preserve_cwd()
def get_tround_venv_context(name, tournament):
    return create_venv(full_tround_path(name, tournament))


@preserve_cwd()
def remove_tround(name, tournament):
    shutil.rmtree(full_tround_path(name, tournament))


@preserve_cwd()
def reload_tround(name, tournament, platform):
    remove_tround(name, tournament)
    create_tround(name, tournament, platform)

