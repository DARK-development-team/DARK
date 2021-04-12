import os
import sys
from celery import shared_task


def execute_queue():
    gupb_git_ssh = 'git@github.com:Prpht/GUPB.git'
    # os.system('cmd /k "git clone {}"'.format(gupb_git_ssh))

    gupb_path = '../GUPB'
    os.chdir(gupb_path)

    # os.system('cmd /k "pip install -r requirements.txt"')
    os.system('cmd /k "python -m gupb"')