import os
import sys
from celery import shared_task

from gupb_queue.models import Queue


def execute_queue(queue_id):
    queue = Queue.objects.get(pk=queue_id)
    platform = queue.platform
    # save current working directory
    current_dir = os.getcwd()
    if not current_dir.endswith('/DARK'):
        current_dir = current_dir[:(current_dir.find('/DARK') + 5)]
        os.chdir(current_dir)
    # set directory for queue logs
    log_directory = f'queue_results'

    # change directory to gupb and execute queue
    os.chdir(f'{platform.name}_{queue_id}')
    os.system(f'python3 -m {platform.package_to_run} -l {log_directory}')

    # restore previous directory
    os.chdir(current_dir)


def get_queue_results(queue_id):

    current_dir = os.getcwd()
    if not current_dir.endswith('/DARK'):
        current_dir = current_dir[:(current_dir.find('/DARK') + 5)]
        os.chdir(current_dir)

    queue = Queue.objects.get(pk=queue_id)

    log_directory = f'{queue.platform.name}_{queue_id}/queue_results'

    if not os.path.exists(log_directory):
        return None

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
