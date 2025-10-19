"""
Script pour peupler la base de données avec des catégories et produits
Exécutez ce script avec: python manage.py shell < populate_products.py
"""

from store.models import Category, Product
from django.utils.text import slugify

# Supprimer les données existantes (optionnel)
print("🗑️ Suppression des données existantes...")
Product.objects.all().delete()
Category.objects.all().delete()

# Créer les catégories
print("\n📦 Création des catégories...")

categories_data = [
    {
        'name': 'DIAMANT FF PAR ID',
        'slug': 'diamant-ff-par-id',
        'description': 'Rechargez vos diamants Free Fire directement par ID. Livraison instantanée!',
        'icon': 'fas fa-gem',
        'order': 1
    },
    {
        'name': 'CODE REDEEM FREE FIRE',
        'slug': 'code-redeem-free-fire',
        'description': 'Codes redeem exclusifs pour Free Fire avec skins et objets rares',
        'icon': 'fas fa-ticket-alt',
        'order': 2
    },
    {
        'name': 'PUBG MOBILE UC',
        'slug': 'pubg-mobile-uc',
        'description': 'Unknown Cash pour PUBG Mobile - Achetez vos UC au meilleur prix',
        'icon': 'fas fa-coins',
        'order': 3
    },
    {
        'name': 'BLOOD STRIKE GOLD',
        'slug': 'blood-strike-gold',
        'description': 'Gold pour Blood Strike - Débloquez des armes et skins exclusifs',
        'icon': 'fas fa-trophy',
        'order': 4
    },
]

categories = {}
for cat_data in categories_data:
    category = Category.objects.create(**cat_data)
    categories[cat_data['slug']] = category
    print(f"✅ Catégorie créée: {category.name}")

# Créer les produits
print("\n🎮 Création des produits...")

products_data = [
    # DIAMANT FF PAR ID
    {
        'name': '100 Diamants Free Fire',
        'description': 'Rechargement instantané de 100 diamants FF. Parfait pour débuter!',
        'price': 500,
        'category': categories['diamant-ff-par-id'],
        'stock': 50,
        'is_featured': True
    },
    {
        'name': '310 Diamants Free Fire',
        'description': '310 diamants + Bonus! Offre populaire pour les joueurs réguliers.',
        'price': 1500,
        'category': categories['diamant-ff-par-id'],
        'stock': 100,
        'is_featured': True
    },
    {
        'name': '520 Diamants Free Fire',
        'description': '520 diamants FF avec bonus exclusif. Meilleur rapport qualité/prix!',
        'price': 2500,
        'category': categories['diamant-ff-par-id'],
        'stock': 75
    },
    {
        'name': '1060 Diamants Free Fire',
        'description': '1060 diamants + Bonus spécial. Pour les vrais gamers!',
        'price': 5000,
        'category': categories['diamant-ff-par-id'],
        'stock': 30,
        'is_featured': True
    },
    {
        'name': '2180 Diamants Free Fire',
        'description': '2180 diamants FF - Pack mega avec bonus exclusifs',
        'price': 10000,
        'category': categories['diamant-ff-par-id'],
        'stock': 20
    },
    {
        'name': '5600 Diamants Free Fire',
        'description': 'Pack ultime! 5600 diamants + Bonus VIP',
        'price': 25000,
        'category': categories['diamant-ff-par-id'],
        'stock': 10,
        'is_featured': True
    },
    
    # CODE REDEEM FREE FIRE
    {
        'name': 'Code Skin Fusil AK47 Légendaire',
        'description': 'Skin AK47 exclusif de rareté Légendaire. Code unique et sécurisé.',
        'price': 3000,
        'category': categories['code-redeem-free-fire'],
        'stock': 15,
        'is_featured': True
    },
    {
        'name': 'Code Bundle Samurai Elite',
        'description': 'Bundle complet Samurai avec tenue, sac à dos et accessoires.',
        'price': 5000,
        'category': categories['code-redeem-free-fire'],
        'stock': 8
    },
    {
        'name': 'Code Emote Dance Exclusive',
        'description': 'Emote de danse ultra rare pour impressionner vos adversaires!',
        'price': 1500,
        'category': categories['code-redeem-free-fire'],
        'stock': 25
    },
    {
        'name': 'Code Pet Panda Légendaire',
        'description': 'Pet Panda avec compétence spéciale et apparence unique.',
        'price': 4000,
        'category': categories['code-redeem-free-fire'],
        'stock': 12,
        'is_featured': True
    },
    {
        'name': 'Code Véhicule Monster Truck',
        'description': 'Skin de véhicule Monster Truck avec effets spéciaux.',
        'price': 3500,
        'category': categories['code-redeem-free-fire'],
        'stock': 10
    },
    {
        'name': 'Code Parachute Dragon',
        'description': 'Parachute Dragon lumineux avec traînée de particules.',
        'price': 2000,
        'category': categories['code-redeem-free-fire'],
        'stock': 20
    },
    
    # PUBG MOBILE UC
    {
        'name': '60 UC PUBG Mobile',
        'description': '60 Unknown Cash pour PUBG Mobile. Livraison rapide!',
        'price': 600,
        'category': categories['pubg-mobile-uc'],
        'stock': 80,
        'is_featured': True
    },
    {
        'name': '325 UC PUBG Mobile',
        'description': '325 UC + Bonus! Idéal pour le Royal Pass.',
        'price': 3000,
        'category': categories['pubg-mobile-uc'],
        'stock': 60
    },
    {
        'name': '660 UC PUBG Mobile',
        'description': '660 UC PUBG Mobile - Pack populaire avec bonus',
        'price': 6000,
        'category': categories['pubg-mobile-uc'],
        'stock': 45,
        'is_featured': True
    },
    {
        'name': '1800 UC PUBG Mobile',
        'description': '1800 UC + Bonus exclusif. Pour les joueurs premium!',
        'price': 16000,
        'category': categories['pubg-mobile-uc'],
        'stock': 25
    },
    {
        'name': '3850 UC PUBG Mobile',
        'description': 'Pack mega 3850 UC avec bonus VIP',
        'price': 33000,
        'category': categories['pubg-mobile-uc'],
        'stock': 15
    },
    {
        'name': '8100 UC PUBG Mobile',
        'description': 'Pack ultime! 8100 UC + Bonus maximum',
        'price': 68000,
        'category': categories['pubg-mobile-uc'],
        'stock': 5,
        'is_featured': True
    },
    
    # BLOOD STRIKE GOLD
    {
        'name': '100 Gold Blood Strike',
        'description': '100 Gold pour Blood Strike. Débloquez vos premières armes!',
        'price': 800,
        'category': categories['blood-strike-gold'],
        'stock': 40,
        'is_featured': True
    },
    {
        'name': '500 Gold Blood Strike',
        'description': '500 Gold + Bonus. Parfait pour les skins premium.',
        'price': 3500,
        'category': categories['blood-strike-gold'],
        'stock': 35
    },
    {
        'name': '1000 Gold Blood Strike',
        'description': '1000 Gold Blood Strike - Offre populaire avec bonus',
        'price': 7000,
        'category': categories['blood-strike-gold'],
        'stock': 28,
        'is_featured': True
    },
    {
        'name': '2500 Gold Blood Strike',
        'description': '2500 Gold + Bonus exclusif. Pour les vrais warriors!',
        'price': 16000,
        'category': categories['blood-strike-gold'],
        'stock': 18
    },
    {
        'name': '5000 Gold Blood Strike',
        'description': 'Pack mega! 5000 Gold avec bonus spéciaux',
        'price': 30000,
        'category': categories['blood-strike-gold'],
        'stock': 12
    },
    {
        'name': '10000 Gold Blood Strike',
        'description': 'Pack ultime! 10000 Gold + Bonus VIP maximum',
        'price': 55000,
        'category': categories['blood-strike-gold'],
        'stock': 6,
        'is_featured': True
    },
]

for product_data in products_data:
    product = Product.objects.create(**product_data)
    featured = "⭐" if product.is_featured else ""
    print(f"✅ Produit créé: {product.name} - {product.price} FCFA {featured}")

print("\n" + "="*60)
print("✨ Base de données peuplée avec succès!")
print(f"📦 {Category.objects.count()} catégories créées")
print(f"🎮 {Product.objects.count()} produits créés")
print("="*60)

# Afficher un résumé par catégorie
print("\n📊 Résumé par catégorie:")
for category in Category.objects.all():
    products_count = category.products.count()
    print(f"  • {category.name}: {products_count} produits") 