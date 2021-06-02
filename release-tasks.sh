#!/bin/bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 -m pip install pip --upgrade
