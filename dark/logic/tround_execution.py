import os
import subprocess
import shutil
import venv

#from celery import task

from dark.models.tournament import TournamentRound
from dark.models.tournament.team import TeamBot
from dark.models.platform import Platform
from .common import data_path
from .tround_utils import \
    tround_relative_local_directory, \
    tround_absolute_local_directory, \
    tround_config_relative_local_directory, \
    tround_config_absolute_local_directory, \
    tround_log_output_absolute_local_directory, \
    tround_log_output_relative_local_directory
from ..common.git import remove_git_repo


class EnvBuilder(venv.EnvBuilder):
    def __init__(self, *args, **kwargs):
        self.context = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        self.context = context


def copy_platform_to_path(platform: Platform, destination):
    shutil.copytree(
        platform.repo.local_directory,
        destination
    )


def prepare_venv(abs_path):
    venv_builder = EnvBuilder(with_pip=True)
    venv_builder.create(f'{abs_path}/venv')
    return venv_builder.context


def install_dependencies(venv_context, requirements_path):
    command = [venv_context.env_exe] + ['-m', 'pip', 'install', '-r', requirements_path]
    return subprocess.check_call(command)


def prepare_environment(path):
    abs_path = f'{os.getcwd()}/{path}'
    venv_context = prepare_venv(abs_path)
    install_dependencies(venv_context, f'{abs_path}/requirements.txt')
    return venv_context


def prepare_environment_for_round(tround: TournamentRound):
    tround_execution_context_path = tround_relative_local_directory(tround.name, tround.tournament.name)
    copy_platform_to_path(tround.platform, tround_execution_context_path)
    return prepare_environment(tround_execution_context_path)


def prepare_config_for_round(tround: TournamentRound):
    bot_objects = TeamBot.objects.filter(tround=tround)

    meta = (tround.tournament.name, tround.name)
    controllers = [(bot.bot_code.path, bot.bot_class_name, bot.team.name) for bot in bot_objects]
    extra_config = {
        'arenas': [
            'archipelago',
            'wasteland',
            'dungeon',
            'fisher_island',
        ],
        'start_balancing': False,
        'visualise': False,
        'show_sight': None,
        'runs_no': 300,
        'profiling_metrics': ['all', 'total', 'avg']
    }
    meta_repr = repr(meta)
    controllers_repr = repr(controllers)
    extra_config_repr = repr(extra_config)

    base_config = open('dark/logic/tround/base_config.py.template', "r")
    tround_config = open(tround_config_relative_local_directory(tround.name, tround.tournament.name), "w")
    for line in base_config:
        line = line.replace('meta = tuple[str, str]()', f'meta = {meta_repr}')
        line = line.replace('controllers = list[tuple[str, str, str]]()', f'controllers = {controllers_repr}')
        line = line.replace('extra_config = dict[str, Any]()', f'extra_config = {extra_config_repr}')
        tround_config.write(line)
    base_config.close()
    tround_config.close()


def execute_round_in_venv(venv_context, tround: TournamentRound):
    package_relative_working_directory = \
        tround_relative_local_directory(tround.name, tround.tournament.name) \
        if tround.platform.platform_relative_wd is None \
        else tround.platform.platform_relative_wd

    package_absolute_working_directory = f'{tround_absolute_local_directory(tround.name, tround.tournament.name)}/' \
                                         f'{package_relative_working_directory}'

    print(package_relative_working_directory)
    print(package_absolute_working_directory)

    package_absolute_path = f'{tround_absolute_local_directory(tround.name, tround.tournament.name)}/' \
                            f'{tround.platform.package_to_run}'
    config_absolute_path = tround_config_absolute_local_directory(tround.name, tround.tournament.name)
    log_output_absolute_path = tround_log_output_absolute_local_directory(tround.name, tround.tournament.name)
    command = [venv_context.env_exe, package_absolute_path, '-c', config_absolute_path, '-l', log_output_absolute_path]

    tround_env_vars = os.environ.copy()
    tround_env_vars['PYTHONPATH'] = package_absolute_working_directory
    print(package_absolute_working_directory)
    sp = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=package_absolute_working_directory, env=tround_env_vars)
    stdout = sp.communicate()[0]
    print(stdout)


def remove_environment(tround: TournamentRound):
    tround_execution_context_path = tround_relative_local_directory(tround.name, tround.tournament.name)
    remove_git_repo(tround_execution_context_path)


def remove_config(tround: TournamentRound):
    tround_config_path = tround_config_relative_local_directory(tround.name, tround.tournament.name)
    os.remove(tround_config_path)


def cleanup_after_execution(tround: TournamentRound):
    remove_environment(tround)
    remove_config(tround)


#@task(bind=True)
def execute_round(tround: TournamentRound):
    #self.update_state(state='PROGRESS', meta={'current': i, 'total': n})
    tround_execution_environment = prepare_environment_for_round(tround)
    prepare_config_for_round(tround)
    execute_round_in_venv(tround_execution_environment, tround)
    cleanup_after_execution(tround)


def get_round_results(tround: TournamentRound):
    log_output_relative_path = tround_log_output_relative_local_directory(tround.name, tround.tournament.name)

    if os.path.isdir(log_output_relative_path):
        result_files = os.listdir(log_output_relative_path)
    else:
        return None

    log_files = [file for file in result_files if os.path.splitext(file)[1] == '.log']
    json_files = [file for file in result_files if os.path.splitext(file)[1] == '.json']
    log_files_paths = [os.path.join(log_output_relative_path, log_file) for log_file in log_files]

    final_run_scores = []
    for log_file_path in log_files_paths:
        with open(log_file_path, 'r') as logs:
            final_run_score = get_final_scores_from_logs(list(logs))
        final_run_scores.append((log_file_path, final_run_score))
    return final_run_scores


def get_final_scores_from_logs(logs):
    results = []

    for line in reversed(logs):
        results.append(line.split(' | '))

    return results