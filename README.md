# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Vérifications de sécurité
python manage.py check --deploy

# Lancer le serveur en production
gunicorn koita_store.wsgi:application --bind 0.0.0.0:8000
git add .
git commit -m "Mise à jour du projet"
git push
python manage.py runserver 