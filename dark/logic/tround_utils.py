import os
import sys

<<<<<<< HEAD:round/round_utils.py

def execute_round():
=======
def execute_tround():
>>>>>>> 354d230... refactored app structure and views + added coverage file + added several tests:dark/logic/tround_utils.py
    # save current working directory
    current_dir = os.getcwd()

<<<<<<< HEAD:round/round_utils.py
    # set directory for queue logs
    log_directory = 'round_results'
=======
    # set directory for tround logs
    log_directory = 'tround_results'
>>>>>>> 354d230... refactored app structure and views + added coverage file + added several tests:dark/logic/tround_utils.py

    # change directory to gupb and execute tround
    os.chdir('GUPB')
    os.system('python -m gupb -l {}'.format(log_directory))

    # restore previous directory
    os.chdir(current_dir)


<<<<<<< HEAD:round/round_utils.py
def get_round_results():
    log_directory = 'GUPB/round_results'
    try:
        result_files = os.listdir(log_directory)
    except FileNotFoundError:
        cwd = os.getcwd()
        files = os.listdir()
        raise FileNotFoundError(f'Current directory is {cwd} with files \n {files}')
=======
def get_tround_results():
    log_directory = 'GUPB/tround_results'
    result_files = os.listdir(log_directory)
>>>>>>> 354d230... refactored app structure and views + added coverage file + added several tests:dark/logic/tround_utils.py

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