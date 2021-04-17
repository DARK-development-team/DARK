web: gunicorn DARK.wsgi
release: git clone https://github.com/Prpht/GUPB.git
release: mkdir GUPB/round_results
release: python manage.py makemigrations team
release: python manage.py makemigrations round
release: python manage.py makemigrations bots
release: python manage.py makemigrations tournament
release: python manage.py migrate
