KOITA_STORE - Version améliorée (scaffold)
----------------------------------------
Ce dépôt contient une structure Django améliorée pour ton projet KOITA_STORE.
Included apps: store, accounts, cart.
Instructions rapides :
  1. Create virtualenv: python -m venv venv
  2. pip install -r requirements.txt
  3. python manage.py migrate
  4. python manage.py createsuperuser  # pour toi (admin)
  5.
Remplace SECRET_KEY et DEBUG dans koita_store/settings.py ou utilise un .env
          # envoyer sur GitHub
git add .
git commit -m "Mise à jour du projet"
git push
 python manage.py runserver