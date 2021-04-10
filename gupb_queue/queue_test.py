import os
import sys


def run():
    gupb_path = '../GUPB'
    os.chdir(gupb_path)
    os.system('cmd /k "python -m gupb"')