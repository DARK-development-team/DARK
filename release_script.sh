git clone https://github.com/Prpht/GUPB.git
mkdir GUPB/round_results
python manage.py makemigrations team
python manage.py makemigrations round
python manage.py makemigrations bots
python manage.py makemigrations tournament
python manage.py migrate