"""
Script pour ajouter des comptes de jeux à la base de données
Exécutez ce script avec: python add_game_accounts.py
"""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'koita_store.settings')
django.setup()

from store.models import Category, Product

def create_accounts_category():
    """Crée la catégorie pour les comptes de jeux"""
    print("📦 Création de la catégorie Comptes de Jeux...")
    
    category, created = Category.objects.get_or_create(
        slug='comptes-de-jeux',
        defaults={
            'name': 'COMPTES DE JEUX',
            'description': 'Comptes de jeux vérifiés, sécurisés et prêts à jouer',
            'icon': 'fas fa-user-shield',
            'order': 5,
            'is_active': True
        }
    )
    
    if created:
        print(f"  ✅ Catégorie créée: {category.name}")
    else:
        print(f"  ℹ️  Catégorie existante: {category.name}")
    
    return category


def create_game_accounts(category):
    """Crée des comptes de jeux de test"""
    print("\n🎮 Création des comptes de jeux...")
    
    accounts_data = [
        # ========================================
        # COMPTES FREE FIRE (10 comptes)
        # ========================================
        {
            'name': 'Compte Free Fire Elite - Niveau 65',
            'description': 'Compte Free Fire niveau 65 avec plus de 50 skins légendaires, dont le bundle Samurai Elite complet. Possède le M1887 Golden Dragon, SCAR Megalodon et plusieurs véhicules exclusifs. Email changeable, 100% sécurisé.',
            'price': 25000,
            'category': category,
            'stock': 5,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte Free Fire VIP - 100k Diamants',
            'description': 'Compte premium avec 100 000 diamants non utilisés ! Niveau 58, plus de 30 bundles incluant le Cobra Bundle, Dragon AK, et le parachute Skyboard exclusif. Idéal pour les collectionneurs.',
            'price': 45000,
            'category': category,
            'stock': 2,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte FF Héroïque - Badge Diamant',
            'description': 'Compte en ligue Héroïque avec badge Diamant permanent. Possède le skin DJ Alok, Jota, K et Chrono. Plus de 40 skins d\'armes rares et 20 véhicules customs. Statistiques impressionnantes.',
            'price': 35000,
            'category': category,
            'stock': 3,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte Free Fire Starter Premium',
            'description': 'Parfait pour débutants : Compte niveau 42 avec le bundle Fire Ranger, DJ Alok, et 15 skins d\'armes légendaires. Inclut 5000 diamants et plusieurs emotes exclusifs.',
            'price': 15000,
            'category': category,
            'stock': 8,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Compte FF Collector - 200+ Skins',
            'description': 'Pour les vrais collectionneurs ! Plus de 200 skins incluant TOUS les bundles saisonniers depuis 2020. Possède les personnages Hayato, Alok, Chrono et K. Véhicules exclusifs et emotes rares.',
            'price': 65000,
            'category': category,
            'stock': 1,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte Free Fire Pro - Toutes Armes Gold',
            'description': 'Compte avec TOUTES les armes en version Golden ! M1887 Gold, AK Gold, AWM Gold, MP40 Gold et plus. Niveau 55, statistiques K/D 5.8. Badge Grand Master.',
            'price': 42000,
            'category': category,
            'stock': 2,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte FF Événement Limité',
            'description': 'Possède des items d\'événements qui ne reviendront JAMAIS : Bundle Booyah Day 2021, Pet Panda Anniversary, Parachute Rainbow. Collection unique !',
            'price': 38000,
            'category': category,
            'stock': 4,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Compte Free Fire Budget - Niveau 50',
            'description': 'Excellent rapport qualité/prix ! Niveau 50, 25 skins d\'armes, 10 bundles sympas, personnages Alok et Kelly. Parfait pour jouer sérieusement sans se ruiner.',
            'price': 12000,
            'category': category,
            'stock': 10,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Compte FF Ultra Rare - Bundle OG',
            'description': 'TRÈS RARE : Possède les bundles originaux (OG) qui n\'existent plus ! Criminal Bundle 2019, Blood Moon Bundle, et le légendaire Cobra Commander. Pour collectionneurs sérieux uniquement.',
            'price': 75000,
            'category': category,
            'stock': 1,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte Free Fire Mid-Tier',
            'description': 'Compte niveau 48 équilibré. Bon mix de skins, quelques personnages utiles (Alok, Moco), et des armes sympas. Idéal pour joueurs intermédiaires.',
            'price': 18000,
            'category': category,
            'stock': 6,
            'is_active': True,
            'is_featured': False
        },
        
        # ========================================
        # COMPTES PUBG MOBILE (8 comptes)
        # ========================================
        {
            'name': 'Compte PUBG Mobile Conqueror - Saison 30',
            'description': 'Rang Conqueror en Squad FPP ! Plus de 60 tenues mythiques, M416 Glacier (max level), AWM Pharaon. Statistiques K/D 6.2, plus de 500 victoires. Email changeable.',
            'price': 55000,
            'category': category,
            'stock': 2,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte PUBG Ace Dominator',
            'description': 'Rang Ace Dominator avec le titre Ace Master. Possède le M416 Golden Lame, Set Pharaon complet, et plus de 40 skins d\'armes mythiques. Casque Jinx et émotes rares.',
            'price': 45000,
            'category': category,
            'stock': 3,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte PUBG VIP - 50k UC',
            'description': 'Incroyable ! 50 000 UC non dépensés sur le compte ! Niveau 75, plusieurs tenues mythiques dont le set Spider-Man exclusif. M416 Glacier et AWM Dragon Hunter. Parfait pour débloquer tout ce que vous voulez.',
            'price': 85000,
            'category': category,
            'stock': 1,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte PUBG Crown Premium',
            'description': 'Rang Crown tier V. Bon compte avec 30+ skins d\'armes dont plusieurs mythiques. Set Royale Pass complets des 3 dernières saisons. Pan Gold et émotes exclusifs.',
            'price': 28000,
            'category': category,
            'stock': 5,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Compte PUBG Collector Edition',
            'description': 'Pour les vrais collectionneurs PUBG : TOUS les Royale Pass depuis la saison 10 ! M416 Glacier maxée, AKM Glacier, plus de 100 tenues dont 25 mythiques. Collection inestimable.',
            'price': 95000,
            'category': category,
            'stock': 1,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte PUBG Starter Plus',
            'description': 'Bon point de départ : Niveau 55, quelques skins sympas, M416 Lab et AKM Runic. Rang Platinum. Idéal pour commencer PUBG sans partir de zéro.',
            'price': 15000,
            'category': category,
            'stock': 8,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Compte PUBG Événement Exclusif',
            'description': 'Possède des items d\'événements limités qui ne reviendront jamais : Tesla Cybertruck, Collaboration Godzilla vs Kong, Set Metro Exodus. Ultra rare !',
            'price': 68000,
            'category': category,
            'stock': 2,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte PUBG Budget - Bon Rapport',
            'description': 'Excellent pour petit budget : Niveau 50, rang Diamond, quelques skins mythiques, M416 Fool et AWM Desert. Plus de 200 victoires. Email changeable.',
            'price': 18000,
            'category': category,
            'stock': 7,
            'is_active': True,
            'is_featured': False
        },
        
        # ========================================
        # COMPTES BLOOD STRIKE (6 comptes)
        # ========================================
        {
            'name': 'Compte Blood Strike Elite - Level 80',
            'description': 'Compte Blood Strike niveau 80 avec TOUTES les armes légendaires débloquées ! AK-47 Dragon Fire, M4A1 Ice Phoenix, AWM Thunder God. Plus de 50 skins et 20 personnages.',
            'price': 32000,
            'category': category,
            'stock': 3,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte Blood Strike VIP Gold',
            'description': 'Abonnement VIP Gold actif pour 6 mois ! Niveau 65, collection complète de skins saisonniers, tous les agents spéciaux débloqués. Statistiques impressionnantes K/D 4.5.',
            'price': 28000,
            'category': category,
            'stock': 4,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte BS Pro Player',
            'description': 'Compte de joueur pro : Rang Master tier I, plus de 1000 victoires, toutes les armes en version Gold. Possède les skins rares du tournoi 2024. Idéal pour la compétition.',
            'price': 42000,
            'category': category,
            'stock': 2,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte Blood Strike Starter',
            'description': 'Parfait pour débuter : Niveau 40, quelques armes légendaires, 10 skins sympas, 5 personnages débloqués. Bon pour apprendre le jeu avec du style !',
            'price': 12000,
            'category': category,
            'stock': 10,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Compte BS Full Legendary',
            'description': 'Toutes les armes en version Légendaire ! Chaque arme du jeu possède son skin légendaire. Collection de rêve pour les fans de Blood Strike. Ultra rare.',
            'price': 58000,
            'category': category,
            'stock': 2,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Compte Blood Strike Mid-Level',
            'description': 'Compte niveau 55 équilibré. Mix de skins légendaires et épiques, plusieurs personnages intéressants, bon rang (Diamond III). Excellent rapport qualité/prix.',
            'price': 16000,
            'category': category,
            'stock': 6,
            'is_active': True,
            'is_featured': False
        },
    ]
    
    created_count = 0
    for account_data in accounts_data:
        product, created = Product.objects.get_or_create(
            name=account_data['name'],
            defaults=account_data
        )
        
        if created:
            created_count += 1
            # Indicateurs visuels
            featured = "⭐" if product.is_featured else "  "
            stock_status = "📦" if product.stock > 5 else "⚠️" if product.stock > 0 else "❌"
            
            print(f"  {featured} {stock_status} {product.name[:50]}... - {product.price:,} FCFA")
    
    print(f"\n📊 Total: {created_count} nouveaux comptes créés")
    return created_count


def display_summary():
    """Affiche un résumé final"""
    print("\n" + "="*70)
    print("🎉 COMPTES DE JEUX AJOUTÉS AVEC SUCCÈS !")
    print("="*70)
    
    # Compter les comptes par catégorie
    account_category = Category.objects.filter(slug='comptes-de-jeux').first()
    
    if account_category:
        total_accounts = Product.objects.filter(category=account_category).count()
        featured_accounts = Product.objects.filter(category=account_category, is_featured=True).count()
        total_stock = sum(p.stock for p in Product.objects.filter(category=account_category))
        total_value = sum(p.price * p.stock for p in Product.objects.filter(category=account_category))
        
        print(f"\n📊 STATISTIQUES :")
        print(f"   • Total comptes : {total_accounts}")
        print(f"   • Comptes vedettes : {featured_accounts}")
        print(f"   • Stock total : {total_stock} unités")
        print(f"   • Valeur totale : {total_value:,} FCFA")
        
        # Répartition par jeu
        ff_count = Product.objects.filter(
            category=account_category, 
            name__icontains='Free Fire'
        ).count()
        pubg_count = Product.objects.filter(
            category=account_category, 
            name__icontains='PUBG'
        ).count()
        bs_count = Product.objects.filter(
            category=account_category, 
            name__icontains='Blood Strike'
        ).count()
        
        print(f"\n🎮 RÉPARTITION PAR JEU :")
        print(f"   • Free Fire : {ff_count} comptes")
        print(f"   • PUBG Mobile : {pubg_count} comptes")
        print(f"   • Blood Strike : {bs_count} comptes")
    
    print("\n" + "="*70)
    print("✅ PROCHAINES ÉTAPES :")
    print("="*70)
    print("1. Lancez le serveur : python manage.py runserver")
    print("2. Visitez la page comptes : http://127.0.0.1:8000/accounts-for-sale/")
    print("3. Testez le carrousel et les filtres")
    print("4. Vérifiez l'admin : http://127.0.0.1:8000/admin/")
    print("="*70 + "\n")


def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("🚀 AJOUT DES COMPTES DE JEUX À LA BASE DE DONNÉES")
    print("="*70 + "\n")
    
    # Étape 1 : Créer la catégorie
    category = create_accounts_category()
    
    # Étape 2 : Créer les comptes
    create_game_accounts(category)
    
    # Étape 3 : Affichage du résumé
    display_summary()


if __name__ == '__main__':
    main()