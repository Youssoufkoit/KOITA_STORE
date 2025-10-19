from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def home(request):
    """Page d'accueil avec tous les produits"""
    products = Product.objects.filter(is_active=True).select_related('category')[:8]
    return render(request, 'store/home.html', {'products': products})

def recharges(request):
    """Page des recharges avec filtrage par catégorie et recherche"""
    # Récupérer toutes les catégories actives
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    # Récupérer les paramètres de requête
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'default')
    
    # Commencer avec tous les produits actifs
    products = Product.objects.filter(is_active=True).select_related('category')
    
    # Filtrer par catégorie si spécifié
    selected_category = None
    if category_slug:
        try:
            selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
            products = products.filter(category=selected_category)
        except:
            pass  # Ignorer si la catégorie n'existe pas
    
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
    
    # Compter le total de produits actifs
    total_products = Product.objects.filter(is_active=True).count()
    
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
    """Page des comptes à vendre"""
    # Récupérer la catégorie "Compte de Jeu" si elle existe
    try:
        compte_category = Category.objects.get(slug='compte-de-jeu')
        products = Product.objects.filter(category=compte_category, is_active=True)
    except Category.DoesNotExist:
        # Si la catégorie n'existe pas, afficher tous les produits actifs
        products = Product.objects.filter(is_active=True)
    
    return render(request, 'store/accounts.html', {'products': products})

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