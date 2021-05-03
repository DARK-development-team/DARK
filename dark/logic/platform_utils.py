import os
import subprocess
from subprocess import Popen, PIPE

from .common import data_path, preserve_cwd
import shutil


def platforms_relto_data_path():
    return 'platforms'


def platform_relto_platforms_path(platform_name):
    return platform_name


def platform_relative_local_directory(platform_name):
    return f'{data_path()}/{platforms_relto_data_path()}/{platform_relto_platforms_path(platform_name)}'


def platform_absolute_local_directory(platform_name):
    return os.path.abspath(f'{data_path()}/{platforms_relto_data_path()}/{platform_relto_platforms_path(platform_name)}')


def get_platform_repo_remote_url(platform_name):
    url = Popen(['git', 'remote', '-v'], stdout=PIPE, cwd=os.getcwd())
    output, _ = url.communicate()
    rc = url.returncode
    if rc != 0:
        return None
    else:
        for line in output.split('\n'):
            name, url, fetch_or_push = list(filter(None, line.split(' ')))
            if 'fetch' in fetch_or_push:
                return url

def ensure_platforms_path():
    def decorator_func(decorated_function):
        def wrapper_func(*args, **kwargs):
            print("git")
            try:
                os.makedirs(f'{data_path()}/{platforms_data_path()}')
            except:
                pass
            return decorated_function(*args, **kwargs)
        return wrapper_func
    return decorator_func


@preserve_cwd()
def clone_platform(platform_name, url, commit):
    subprocess.call(['git', 'clone', url, platform_relative_local_directory(platform_name)], cwd=os.getcwd())
    subprocess.call(['git', 'checkout', commit], cwd=platform_absolute_local_directory(platform_name))

@preserve_cwd()
def remove_platform(platform_name):
    shutil.rmtree(platform_relative_local_directory(platform_name))


@preserve_cwd()
def update_platform_url(platform_name, url, commit):
    remove_platform(platform_name)
    clone_platform(platform_name, url, commit)


@preserve_cwd()
def update_platform_name(old_platform_name, new_platform_name):
    shutil.move(
        platform_absolute_local_directory(old_platform_name),
        platform_absolute_local_directory(new_platform_name)
    )


@preserve_cwd()
def update_platform_commit(platform_name, commit):
    subprocess.call(['git', 'checkout', commit], cwd=platform_absolute_local_directory(platform_name))
