import os


def clone_repo(dir, url, commit):
    current_dir = os.getcwd()
    if not current_dir.endswith('/DARK'):
        current_dir = current_dir[:(current_dir.find('/DARK') + 5)]
        os.chdir(current_dir)
    os.system(f'git clone {url} {dir}')
    os.chdir(dir)
    os.system(f'git checkout {commit}')
    os.system('pip3 install -r requirements.txt')
    os.chdir(current_dir)
