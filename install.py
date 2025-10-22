# install.py
import os
import sys
import django

def setup_project():
    """Script de configuration automatique du projet"""
    
    # Vérifier si le fichier .env existe
    if not os.path.exists('.env'):
        print("📝 Création du fichier .env...")
        with open('.env', 'w') as f:
            f.write("""SECRET_KEY=votre_clé_secrète_très_longue_ici_123456789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-application
""")
        print("✅ Fichier .env créé - Pensez à modifier les valeurs!")
    
    # Installer les dépendances
    print("📦 Installation des dépendances...")
    os.system('pip install -r requirements.txt')
    
    # Appliquer les migrations
    print("🗃️ Application des migrations...")
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    
    # Créer un superutilisateur
    print("👤 Création d'un superutilisateur...")
    os.system('python manage.py createsuperuser')
    
    # Collecter les fichiers statiques
    print("📁 Collecte des fichiers statiques...")
    os.system('python manage.py collectstatic --noinput')
    
    print("""
🎉 Installation terminée !

Prochaines étapes :
1. 📧 Configurez vos emails dans le fichier .env
2. 🚀 Lancez le serveur : python manage.py runserver
3. 🌐 Accédez à http://localhost:8000

Bonne chance avec KOITA_STORE! 🎮
""")

if __name__ == "__main__":
    setup_project()