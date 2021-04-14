import os
import sys
from celery import shared_task


def execute_queue():
    # save current working directory
    curent_dir = os.getcwd()

    # set directory for queue logs
    log_directory = 'queue_results'

    # change directory to gupb and execute queue
    os.chdir('GUPB')
    os.system('python -m gupb -l {}'.format(log_directory))

    # restore previous directory
    os.chdir(curent_dir)


def get_queue_results():
    log_directory = 'GUPB/queue_results'
    result_files = os.listdir(log_directory)

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
