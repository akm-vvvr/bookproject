set -o errexit
pip install -r requirements.html
python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 manage.py superuser