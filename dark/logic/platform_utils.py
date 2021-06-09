import os
import requirements
from .common import data_path


def platforms_relto_data_path():
    return 'platforms'


def platform_relto_platforms_path(platform_name):
    return platform_name


def platform_relative_local_directory(platform_name):
    return f'{data_path()}/{platforms_relto_data_path()}/{platform_relto_platforms_path(platform_name)}'


def platform_absolute_local_directory(platform_name):
    return os.path.abspath(platform_relative_local_directory(platform_name))


def get_platform_requirements(platform):
    req_path = platform.repo.local_directory + '/requirements.txt'
    requirements_list = []
    with open(req_path) as req_file:
        for req in requirements.parse(req_file):
            requirements_list.append(req)
    return requirements_list
