#!/bin/bash
git clone https://github.com/Prpht/GUPB.git
mkdir GUPB/round_results
python manage.py makemigrations
python manage.py migrate
