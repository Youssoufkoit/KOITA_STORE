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
 # store/views.py - Mise à jour de la fonction accounts_for_sale

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def home(request):
    """Page d'accueil avec tous les produits"""
    products = Product.objects.filter(is_active=True).select_related('category')[:8]
    return render(request, 'store/home.html', {'products': products})


def recharges(request):
    """Page des recharges avec filtrage par catégorie et recherche"""
    # Récupérer toutes les catégories actives SAUF "Compte de Jeu"
    categories = Category.objects.filter(
        is_active=True
    ).exclude(
        slug__icontains='compte'
    ).order_by('order', 'name')
    
    # Récupérer les paramètres de requête
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'default')
    
    # Commencer avec tous les produits actifs SAUF les comptes
    products = Product.objects.filter(
        is_active=True
    ).exclude(
        category__slug__icontains='compte'
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
    
    # Compter le total de produits actifs (hors comptes)
    total_products = Product.objects.filter(
        is_active=True
    ).exclude(
        category__slug__icontains='compte'
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
    """Page des comptes à vendre - MISE À JOUR"""
    # Récupérer UNIQUEMENT les catégories de comptes
    account_categories = Category.objects.filter(
        is_active=True,
        slug__icontains='compte'  # ou name__icontains='compte'
    )
    
    # Si aucune catégorie "compte" n'existe, créer une catégorie par défaut
    if not account_categories.exists():
        # Filtrer tous les produits actifs qui pourraient être des comptes
        # (basé sur le nom ou la description contenant "compte")
        products = Product.objects.filter(
            Q(is_active=True) & (
                Q(name__icontains='compte') | 
                Q(description__icontains='compte')
            )
        ).select_related('category')
    else:
        # Récupérer les produits des catégories de comptes
        products = Product.objects.filter(
            category__in=account_categories,
            is_active=True
        ).select_related('category')
    
    # Filtrage par paramètres GET (optionnel)
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
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