import os
from .common import data_path


def tournaments_relto_data_path():
    return 'tournaments'


def tournament_relto_data_path(tournament_name):
    return f'{tournaments_relto_data_path()}/{tournament_name}'


def tround_relto_tournament_path(tround_name):
    return tround_name


def tround_relative_local_directory(tround_name, tournament_name):
    return f'{data_path()}/{tournament_relto_data_path(tournament_name)}/{tround_relto_tournament_path(tround_name)}'


def tround_absolute_local_directory(tround_name, tournament_name):
    return os.path.abspath(tround_relative_local_directory(tround_name, tournament_name))


def tround_config_relative_local_directory(tround_name, tournament_name):
    return f'{data_path()}/{tournament_relto_data_path(tournament_name)}/{tround_relto_tournament_path(tround_name)}_config.py'


def tround_config_absolute_local_directory(tround_name, tournament_name):
    return os.path.abspath(tround_config_relative_local_directory(tround_name, tournament_name))


def tround_log_output_relative_local_directory(tround_name, tournament_name):
    return f'{data_path()}/{tournament_relto_data_path(tournament_name)}/' \
           f'{tround_relto_tournament_path(tround_name)}_queue_execution_logs'


def tround_log_output_absolute_local_directory(tround_name, tournament_name):
    return os.path.abspath(tround_log_output_relative_local_directory(tround_name, tournament_name))
