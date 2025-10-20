from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Product, Category


def home(request):
    """Page d'accueil avec tous les produits"""
    products = Product.objects.filter(is_active=True).select_related('category')[:8]
    return render(request, 'store/home.html', {'products': products})


def recharges(request):
    """
    Page des recharges - UNIQUEMENT les produits qui NE SONT PAS des comptes
    On filtre en EXCLUANT les catégories contenant 'compte' dans leur nom/slug
    """
    
    # Récupérer UNIQUEMENT les catégories qui ne sont PAS des comptes
    categories = Category.objects.filter(
        is_active=True
    ).exclude(
        Q(slug__icontains='compte') | Q(name__icontains='compte')
    ).order_by('order', 'name')
    
    # Récupérer les paramètres de requête
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'default')
    
    # Commencer avec UNIQUEMENT les produits de catégories RECHARGE (exclure comptes)
    products = Product.objects.filter(
        is_active=True
    ).exclude(
        Q(category__slug__icontains='compte') | Q(category__name__icontains='compte')
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
        is_active=True
    ).exclude(
        Q(category__slug__icontains='compte') | Q(category__name__icontains='compte')
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
    """
    Page des comptes à vendre - UNIQUEMENT les produits de type COMPTE
    On filtre en INCLUANT seulement les catégories contenant 'compte'
    """
    
    # Récupérer UNIQUEMENT les catégories de type COMPTE
    account_categories = Category.objects.filter(
        is_active=True
    ).filter(
        Q(slug__icontains='compte') | Q(name__icontains='compte')
    ).order_by('order', 'name')
    
    # Récupérer UNIQUEMENT les produits des catégories de type COMPTE
    products = Product.objects.filter(
        is_active=True
    ).filter(
        Q(category__slug__icontains='compte') | Q(category__name__icontains='compte')
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
    """Page de détail d'un produit avec support REDEEM"""
    product = get_object_or_404(Product, pk=pk)
    
    # Produits similaires de la même catégorie
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk).select_related('category')[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'is_redeem_product': product.is_redeem_product,
    }
    return render(request, 'store/product_detail.html', context)


def contact(request):
    """Page de contact avec envoi d'email"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Envoyer l'email
        full_message = f"""
Message de {name} ({email})
Sujet: {subject}

Message:
{message}
        """
        
        try:
            send_mail(
                subject=f"Contact KOITA_STORE: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, '✅ Votre message a été envoyé avec succès!')
        except Exception as e:
            messages.error(request, f'❌ Erreur lors de l\'envoi du message: {str(e)}')
    
    return render(request, 'contact/contact.html')