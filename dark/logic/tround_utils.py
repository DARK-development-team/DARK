import os

from dark.models.tournament import TournamentRound


def execute_round(round_id):
    tround = TournamentRound.objects.get(pk=round_id)
    platform = tround.platform
    # save current working directory
    current_dir = os.getcwd()
    if not current_dir.endswith('/DARK'):
        current_dir = current_dir[:(current_dir.find('/DARK') + 5)]
        os.chdir(current_dir)
    # set directory for round logs
    log_directory = f'round_results'

    # change directory to gupb and execute round
    os.chdir(f'{platform.name}_{round_id}')
    os.system(f'python3 -m {platform.package_to_run} -l {log_directory}')

    os.chdir(current_dir)


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
