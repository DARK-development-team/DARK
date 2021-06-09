import os
import stat
import shutil

def chmod_readonly_git_files(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)

def remove_git_repo(path):
    chmod_readonly_git_files(path)
    shutil.rmtree(path)
