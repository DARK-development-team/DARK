import os
import subprocess
import sys

from dark.models.tournament import TournamentRound
from dark.models.tournament.team import TeamBot
from .common import data_path, preserve_cwd
from .tround_utils import full_tround_path, get_tround_venv_context


def prepare_config_for_round(tround: TournamentRound):
    bot_objects = TeamBot.objects.filter(tround=tround)

    bots = [(bot.bot_code.path, bot.bot_class_name) for bot in bot_objects]
    profiling_metrics = [] # to be customized
    arenas = ['archipelago', 'wasteland', 'dungeon', 'fisher_island'] # to be customized

    bots_r = str(bots)
    profiling_metrics_r = str(profiling_metrics)
    arenas_r = str(arenas)

    base_config = open('dark/logic/base_config.py', "r")
    tround_config = open(f'{full_tround_path(tround.name, tround.tournament)}/config.py', "w")
    for line in base_config:
        line = line.replace('bots = []', f'bots = {bots_r}')
        line = line.replace('arenas = []', f'arenas = {arenas_r}')
        line = line.replace('profiling_metrics = []', f'profiling_metrics = {profiling_metrics_r}')
        tround_config.write(line)
    base_config.close()
    tround_config.close()


@preserve_cwd()
def exec_in_venv(tround: TournamentRound):
    context = get_tround_venv_context(tround.name, tround.tournament)
    package_working_directory = f'{full_tround_path(tround.name, tround.tournament)}'
    package_relative_path = f'{tround.platform.package_to_run}'
    config_relative_path = f'config.py'
    command = [context.env_exe, package_relative_path,
               '-c', config_relative_path]

    tround_env = os.environ.copy()
    tround_env['PYTHONPATH'] = os.path.abspath(package_working_directory)
    sp = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=package_working_directory, env=tround_env)
    stdout = sp.communicate()[0]
    print(stdout)


@preserve_cwd()
def execute_round(tround: TournamentRound):
    prepare_config_for_round(tround)
    exec_in_venv(tround)


def get_round_results(round_id):
    tround = TournamentRound.objects.get(pk=round_id)

    log_directory = f'{tround.platform.name}_{round_id}/round_results'
    try:
        result_files = os.listdir(log_directory)
    except FileNotFoundError:
        cwd = os.getcwd()
        files = os.listdir()
        raise FileNotFoundError(f'Current directory is {cwd} with files \n {files}')

    if not result_files:
        return None

    result_files = [file for file in result_files if file[-3:] == 'log']
    file_path = log_directory + '/' + result_files[0]

    with open(file_path, 'r') as logs:
        final_scores = get_final_scores_from_logs(list(logs))

    return final_scores


def get_final_scores_from_logs(logs):
    results = []
    for line in reversed(logs):
        results.append(line.split(' | ')[3])
        if len(results) == 4:
            break

    return sorted(results)