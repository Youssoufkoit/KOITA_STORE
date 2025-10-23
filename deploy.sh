#!/bin/bash

# ==================================================
# KOITA_STORE - SCRIPT DE DÉPLOIEMENT
# ==================================================

echo "🚀 Démarrage du déploiement de KOITA_STORE..."

# ==================================================
# 1. VÉRIFICATIONS PRÉLIMINAIRES
# ==================================================
echo "✅ Vérification de l'environnement..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérifier pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip n'est pas installé"
    exit 1
fi

# ==================================================
# 2. INSTALLATION DES DÉPENDANCES
# ==================================================
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# ==================================================
# 3. CONFIGURATION DE L'ENVIRONNEMENT
# ==================================================
echo "⚙️ Configuration de l'environnement..."

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "⚠️ Fichier .env non trouvé. Création à partir de .env.example..."
    cp .env.example .env
    echo "⚠️ IMPORTANT: Éditer le fichier .env avec vos vraies valeurs!"
    exit 1
fi

# ==================================================
# 4. MIGRATION DE LA BASE DE DONNÉES
# ==================================================
echo "🗄️ Migration de la base de données..."
python manage.py makemigrations
python manage.py migrate

# ==================================================
# 5. COLLECTE DES FICHIERS STATIQUES
# ==================================================
echo "📂 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# ==================================================
# 6. CRÉATION DU SUPERUTILISATEUR (Optionnel)
# ==================================================
echo "👤 Voulez-vous créer un superutilisateur? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# ==================================================
# 7. TESTS (Optionnel)
# ==================================================
echo "🧪 Voulez-vous lancer les tests? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    python manage.py test
fi

# ==================================================
# 8. VÉRIFICATIONS DE SÉCURITÉ
# ==================================================
echo "🔒 Vérifications de sécurité..."
python manage.py check --deploy

# ==================================================
# 9. DÉMARRAGE DU SERVEUR
# ==================================================
echo "✅ Déploiement terminé!"
echo ""
echo "Pour démarrer le serveur en production:"
echo "  gunicorn koita_store.wsgi:application --bind 0.0.0.0:8000"
echo ""
echo "Ou pour le développement:"
echo "  python manage.py runserver"