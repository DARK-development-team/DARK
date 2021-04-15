import os


def clone_repo(dir, url):
    current_dir = os.getcwd()
    os.system(f'git clone {url} {dir}')
    os.chdir(dir)
    os.system('pip3 install -r requirements.txt')
    os.chdir(current_dir)
