  1. Create virtualenv: python -m venv venv
  2. pip install -r requirements.txt
  3. python manage.py migrate
  4. python manage.py createsuperuser  # pour toi (admin)
  5.
git add .
git commit -m "Mise à jour du projet"
git push
 python manage.py runserver