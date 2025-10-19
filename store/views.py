from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def home(request):
    """Page d'accueil avec tous les produits"""
    products = Product.objects.filter(is_active=True).select_related('category')[:8]
    return render(request, 'store/home.html', {'products': products})


def recharges(request):
    """Page des recharges - UNIQUEMENT les produits de type 'recharge'"""
    
    # Récupérer UNIQUEMENT les catégories de type RECHARGE
    categories = Category.objects.filter(
        is_active=True,
        category_type='recharge'  # Utilise le nouveau champ category_type
    ).order_by('order', 'name')
    
    # Récupérer les paramètres de requête
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'default')
    
    # Commencer avec UNIQUEMENT les produits de catégories RECHARGE
    products = Product.objects.filter(
        is_active=True,
        category__category_type='recharge'  # Filtre par type de catégorie
    ).select_related('category')
    
    # Filtrer par catégorie si spécifié
    selected_category = None
    if category_slug:
        try:
            selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
            products = products.filter(category=selected_category)
        except:
            pass
    
    # Filtrer par recherche si spécifié
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Trier les résultats
    if sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # default
        products = products.order_by('-is_featured', '-created_at')
    
    # Compter le total de produits RECHARGE actifs
    total_products = Product.objects.filter(
        is_active=True,
        category__category_type='recharge'
    ).count()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_products': total_products,
    }
    
    return render(request, 'store/recharges.html', context)


def accounts_for_sale(request):
    """Page des comptes à vendre - UNIQUEMENT les produits de type 'account'"""
    
    # Récupérer UNIQUEMENT les catégories de type COMPTE
    account_categories = Category.objects.filter(
        is_active=True,
        category_type='account'  # ⚠️ IMPORTANT : Utilise le champ category_type
    ).order_by('order', 'name')
    
    # Récupérer UNIQUEMENT les produits des catégories de type COMPTE
    products = Product.objects.filter(
        is_active=True,
        category__category_type='account'  # ⚠️ IMPORTANT : Filtre par type
    ).select_related('category')
    
    # Filtrage par catégorie spécifique (optionnel)
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    # Recherche (optionnel)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(account_rank__icontains=search_query)
        )
    
    # Trier par défaut : vedettes puis par date
    products = products.order_by('-is_featured', '-created_at')
    
    # Récupérer les comptes vedettes pour le carrousel
    featured_products = products.filter(is_featured=True)[:6]
    
    # Si aucun produit vedette, prendre les 6 premiers
    if not featured_products.exists():
        featured_products = products[:6]
    
    context = {
        'products': products,
        'featured_products': featured_products,
        'account_categories': account_categories,
        'search_query': search_query,
    }
    
    return render(request, 'store/accounts.html', context)


def product_detail(request, pk):
    """Page de détail d'un produit"""
    product = get_object_or_404(Product, pk=pk)
    
    # Produits similaires de la même catégorie
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk).select_related('category')[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def contact(request):
    """Page de contact"""
    return render(request, 'contact/contact.html')