import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'koita_store.settings')
django.setup()

from store.models import Category, Product

def create_test_data():
    print("🔄 Création des données de test...")
    
    # Créer les catégories
    categories = [
        {'name': 'Diamants', 'slug': 'diamants'},
        {'name': 'Free Fire', 'slug': 'free-fire'}, 
        {'name': 'PUBG Mobile', 'slug': 'pubg-mobile'},
        {'name': 'Blood Strike', 'slug': 'blood-strike'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'slug': cat_data['slug']}
        )
        if created:
            print(f'✅ Catégorie créée: {category.name}')
    
    # Récupérer les catégories
    diamants_cat = Category.objects.get(slug='diamants')
    free_fire_cat = Category.objects.get(slug='free-fire')
    pubg_cat = Category.objects.get(slug='pubg-mobile')
    blood_strike_cat = Category.objects.get(slug='blood-strike')
    
    # Produits de test simples
    products = [
        # Diamants
        {'name': '50 Diamants Free Fire', 'price': 4.99, 'type': 'diamant', 'category': diamants_cat},
        {'name': '100 Diamants Free Fire', 'price': 9.99, 'type': 'diamant', 'category': diamants_cat},
        
        # Free Fire
        {'name': 'Code Redeem 100 Diamants', 'price': 2.99, 'type': 'free_fire', 'category': free_fire_cat},
        {'name': 'Code Redeem 300 Diamants', 'price': 7.99, 'type': 'free_fire', 'category': free_fire_cat},
        
        # PUBG Mobile
        {'name': '60 UC PUBG Mobile', 'price': 0.99, 'type': 'pubg', 'category': pubg_cat},
        {'name': '325 UC PUBG Mobile', 'price': 4.99, 'type': 'pubg', 'category': pubg_cat},
        
        # Blood Strike
        {'name': '100 Gold Blood Strike', 'price': 0.99, 'type': 'blood_strike', 'category': blood_strike_cat},
        {'name': '550 Gold Blood Strike', 'price': 4.99, 'type': 'blood_strike', 'category': blood_strike_cat},
    ]
    
    for product_data in products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'price': product_data['price'],
                'product_type': product_data['type'],
                'category': product_data['category'],
                'stock': 100,
                'is_active': True,
                'description': f'Recharge {product_data["name"]} - Livraison instantanée'
            }
        )
        if created:
            print(f'✅ Produit créé: {product.name}')
    
    print("🎉 Données de test créées avec succès!")
    print(f"📊 Total catégories: {Category.objects.count()}")
    print(f"📊 Total produits: {Product.objects.count()}")

if __name__ == '__main__':
    create_test_data()