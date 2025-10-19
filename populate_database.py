"""
Script pour peupler automatiquement la base de données avec 4 catégories et 24 produits
Exécutez ce script avec: python populate_database.py
"""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'koita_store.settings')
django.setup()

from store.models import Category, Product

def clear_database():
    """Nettoie la base de données"""
    print("🗑️  Nettoyage de la base de données...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    print("✅ Base de données nettoyée\n")

def create_categories():
    """Crée les 4 catégories principales"""
    print("📦 Création des catégories...")
    
    categories_data = [
        {
            'name': 'DIAMANT FF PAR ID',
            'slug': 'diamant-ff-par-id',
            'description': 'Rechargez vos diamants Free Fire directement par ID. Livraison instantanée en moins de 5 minutes !',
            'icon': 'fas fa-gem',
            'order': 1
        },
        {
            'name': 'CODE REDEEM FREE FIRE',
            'slug': 'code-redeem-free-fire',
            'description': 'Codes redeem exclusifs pour Free Fire avec skins rares, bundles et émotes légendaires',
            'icon': 'fas fa-ticket-alt',
            'order': 2
        },
        {
            'name': 'PUBG MOBILE UC',
            'slug': 'pubg-mobile-uc',
            'description': 'Unknown Cash pour PUBG Mobile. Achetez vos UC au meilleur prix avec livraison rapide',
            'icon': 'fas fa-coins',
            'order': 3
        },
        {
            'name': 'BLOOD STRIKE GOLD',
            'slug': 'blood-strike-gold',
            'description': 'Gold pour Blood Strike. Débloquez des armes et skins exclusifs pour dominer la partie',
            'icon': 'fas fa-trophy',
            'order': 4
        },
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = Category.objects.create(**cat_data)
        categories[cat_data['slug']] = category
        print(f"  ✅ {category.name}")
    
    print(f"\n📊 Total: {Category.objects.count()} catégories créées\n")
    return categories

def create_products(categories):
    """Crée 24 produits (6 par catégorie)"""
    print("🎮 Création des produits...")
    
    products_data = [
        # ========================================
        # DIAMANT FF PAR ID (6 produits)
        # ========================================
        {
            'name': '50 Diamants Free Fire',
            'description': 'Pack starter parfait pour débuter ! 50 diamants livrés instantanément sur votre compte Free Fire via votre ID.',
            'price': 500,
            'category': categories['diamant-ff-par-id'],
            'stock': 100,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': '100 Diamants Free Fire',
            'description': 'Rechargement instantané de 100 diamants FF. Idéal pour acheter le Weekly Pass ou des skins basiques.',
            'price': 950,
            'category': categories['diamant-ff-par-id'],
            'stock': 150,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '310 Diamants Free Fire',
            'description': '310 diamants + BONUS ! Offre populaire pour les joueurs réguliers. Parfait pour le Monthly Pass.',
            'price': 2800,
            'category': categories['diamant-ff-par-id'],
            'stock': 200,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '520 Diamants Free Fire',
            'description': '520 diamants FF avec bonus exclusif. Meilleur rapport qualité/prix ! Achetez des bundles premium.',
            'price': 4500,
            'category': categories['diamant-ff-par-id'],
            'stock': 180,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '1060 Diamants Free Fire',
            'description': '1060 diamants + Bonus spécial. Pour les vrais gamers qui veulent tout débloquer sans limites.',
            'price': 9000,
            'category': categories['diamant-ff-par-id'],
            'stock': 120,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': '2180 Diamants Free Fire',
            'description': 'Pack MEGA ! 2180 diamants + Bonus VIP exclusif. Devenez une légende sur Free Fire avec ce pack ultime.',
            'price': 18000,
            'category': categories['diamant-ff-par-id'],
            'stock': 80,
            'is_active': True,
            'is_featured': True
        },
        
        # ========================================
        # CODE REDEEM FREE FIRE (6 produits)
        # ========================================
        {
            'name': 'Code Skin Fusil AK47 Légendaire',
            'description': 'Skin AK47 exclusif de rareté Légendaire avec effets spéciaux ! Code unique garanti valide.',
            'price': 3500,
            'category': categories['code-redeem-free-fire'],
            'stock': 25,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Code Bundle Samurai Elite',
            'description': 'Bundle complet Samurai Elite : tenue, masque, sac à dos, parachute et emote. Set ultra rare !',
            'price': 5500,
            'category': categories['code-redeem-free-fire'],
            'stock': 15,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Code Emote Dance Exclusive',
            'description': 'Emote de danse ultra rare pour impressionner vos adversaires ! Animation unique et stylée.',
            'price': 1800,
            'category': categories['code-redeem-free-fire'],
            'stock': 40,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Code Pet Panda Légendaire',
            'description': 'Pet Panda avec compétence spéciale EP++ et apparence kawaii. Votre meilleur allié en partie !',
            'price': 4200,
            'category': categories['code-redeem-free-fire'],
            'stock': 20,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Code Véhicule Monster Truck',
            'description': 'Skin de véhicule Monster Truck avec effets spéciaux et boost de vitesse visuel. Écrasez la concurrence !',
            'price': 3800,
            'category': categories['code-redeem-free-fire'],
            'stock': 18,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': 'Code Parachute Dragon Volant',
            'description': 'Parachute Dragon lumineux avec traînée de particules dorées. Atterrissez avec style !',
            'price': 2500,
            'category': categories['code-redeem-free-fire'],
            'stock': 35,
            'is_active': True,
            'is_featured': False
        },
        
        # ========================================
        # PUBG MOBILE UC (6 produits)
        # ========================================
        {
            'name': '60 UC PUBG Mobile',
            'description': '60 Unknown Cash pour PUBG Mobile. Livraison rapide ! Parfait pour le Royale Pass Lite.',
            'price': 600,
            'category': categories['pubg-mobile-uc'],
            'stock': 150,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '325 UC PUBG Mobile',
            'description': '325 UC + Bonus ! Idéal pour le Royale Pass complet. Débloquez toutes les récompenses premium.',
            'price': 3000,
            'category': categories['pubg-mobile-uc'],
            'stock': 120,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '660 UC PUBG Mobile',
            'description': '660 UC PUBG Mobile - Pack populaire avec bonus. Achetez des caisses et des tenues exclusives.',
            'price': 6000,
            'category': categories['pubg-mobile-uc'],
            'stock': 100,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '1800 UC PUBG Mobile',
            'description': '1800 UC + Bonus exclusif. Pour les joueurs premium qui veulent les meilleurs skins du jeu !',
            'price': 16000,
            'category': categories['pubg-mobile-uc'],
            'stock': 70,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': '3850 UC PUBG Mobile',
            'description': 'Pack mega 3850 UC avec bonus VIP. Dominez le classement avec les tenues les plus rares !',
            'price': 33000,
            'category': categories['pubg-mobile-uc'],
            'stock': 45,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': '8100 UC PUBG Mobile',
            'description': 'Pack ULTIME ! 8100 UC + Bonus maximum. Devenez une légende PUBG avec ce pack exceptionnel.',
            'price': 68000,
            'category': categories['pubg-mobile-uc'],
            'stock': 25,
            'is_active': True,
            'is_featured': True
        },
        
        # ========================================
        # BLOOD STRIKE GOLD (6 produits)
        # ========================================
        {
            'name': '100 Gold Blood Strike',
            'description': '100 Gold pour Blood Strike. Débloquez vos premières armes légendaires et commencez à dominer !',
            'price': 800,
            'category': categories['blood-strike-gold'],
            'stock': 80,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '500 Gold Blood Strike',
            'description': '500 Gold + Bonus. Parfait pour les skins premium et les Battle Pass. Excellent rapport qualité/prix !',
            'price': 3800,
            'category': categories['blood-strike-gold'],
            'stock': 65,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '1000 Gold Blood Strike',
            'description': '1000 Gold Blood Strike - Offre populaire avec bonus généreux. Débloquez plusieurs armes mythiques.',
            'price': 7500,
            'category': categories['blood-strike-gold'],
            'stock': 55,
            'is_active': True,
            'is_featured': True
        },
        {
            'name': '2500 Gold Blood Strike',
            'description': '2500 Gold + Bonus exclusif. Pour les vrais warriors qui veulent la collection complète !',
            'price': 17000,
            'category': categories['blood-strike-gold'],
            'stock': 40,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': '5000 Gold Blood Strike',
            'description': 'Pack mega ! 5000 Gold avec bonus spéciaux. Toutes les armes et tous les skins à votre portée.',
            'price': 32000,
            'category': categories['blood-strike-gold'],
            'stock': 30,
            'is_active': True,
            'is_featured': False
        },
        {
            'name': '10000 Gold Blood Strike',
            'description': 'Pack ULTIME ! 10000 Gold + Bonus VIP maximum. Soyez le joueur le plus stylé du serveur !',
            'price': 60000,
            'category': categories['blood-strike-gold'],
            'stock': 15,
            'is_active': True,
            'is_featured': True
        },
    ]
    
    product_count = 0
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        product_count += 1
        
        # Affichage avec indicateurs
        featured = "⭐" if product.is_featured else "  "
        stock_status = "📦" if product.stock > 50 else "⚠️" if product.stock > 0 else "❌"
        
        print(f"  {featured} {stock_status} {product.name} - {product.price:,} FCFA")
    
    print(f"\n📊 Total: {Product.objects.count()} produits créés\n")

def display_summary():
    """Affiche un résumé final"""
    print("="*70)
    print("🎉 BASE DE DONNÉES PEUPLÉE AVEC SUCCÈS !")
    print("="*70)
    
    print(f"\n📦 CATÉGORIES : {Category.objects.count()}")
    for category in Category.objects.all().order_by('order'):
        product_count = category.products.count()
        print(f"   • {category.name}: {product_count} produits")
    
    print(f"\n🎮 PRODUITS : {Product.objects.count()}")
    print(f"   • Produits vedettes : {Product.objects.filter(is_featured=True).count()}")
    print(f"   • Stock total disponible : {sum(p.stock for p in Product.objects.all()):,} unités")
    
    total_value = sum(p.price * p.stock for p in Product.objects.all())
    print(f"   • Valeur totale du stock : {total_value:,} FCFA")
    
    print("\n" + "="*70)
    print("✅ PROCHAINES ÉTAPES :")
    print("="*70)
    print("1. Lancez le serveur : python manage.py runserver")
    print("2. Accédez à la page recharges : http://127.0.0.1:8000/recharges/")
    print("3. Testez les filtres par catégorie et la recherche")
    print("4. Connectez-vous à l'admin : http://127.0.0.1:8000/admin/")
    print("="*70 + "\n")

def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("🚀 SCRIPT DE PEUPLEMENT DE LA BASE DE DONNÉES")
    print("="*70 + "\n")
    
    # Étape 1 : Nettoyage
    clear_database()
    
    # Étape 2 : Création des catégories
    categories = create_categories()
    
    # Étape 3 : Création des produits
    create_products(categories)
    
    # Étape 4 : Affichage du résumé
    display_summary()

if __name__ == '__main__':
    main()