import os
from .common import data_path, preserve_cwd
import shutil


def platforms_data_path():
    return 'platforms'


def platform_platforms_path(platform_name):
    return platform_name


def full_platform_path(platform_name):
    return f'{data_path()}/{platforms_data_path()}/{platform_platforms_path(platform_name)}'


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
@ensure_platforms_path()
def pull_platform(platform_name, url, commit):
    os.chdir(data_path())
    os.chdir(platforms_data_path())
    os.system(f'git clone {url} {platform_platforms_path(platform_name)}')
    os.chdir(platform_platforms_path(platform_name))
    os.system(f'git checkout {commit}')

@preserve_cwd()
@ensure_platforms_path()
def remove_platform(platform_name):
    os.chdir(data_path())
    os.chdir(platforms_data_path())
    shutil.rmtree(platform_platforms_path(platform_name))

@preserve_cwd()
@ensure_platforms_path()
def reload_platform(platform_name, url, commit):
    remove_platform(platform_name)
    pull_platform(platform_name, url, commit)
