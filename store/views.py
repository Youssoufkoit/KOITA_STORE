from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Order, OrderItem, Notification
from scripts.shop2game_redeem import Shop2GameRedeemer
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Page d'accueil avec tous les produits et catégories"""
    # Récupérer les produits actifs
    products = Product.objects.filter(is_active=True).select_related('category')[:8]
    
    # Récupérer les catégories de recharges (exclure les comptes) pour l'accueil
    recharge_categories = Category.objects.filter(
        is_active=True
    ).exclude(
        Q(slug__icontains='compte') | Q(name__icontains='compte')
    ).order_by('order', 'name')[:10]  # Limiter à 10 catégories max
    
    context = {
        'products': products,
        'recharge_categories': recharge_categories,
    }
    return render(request, 'store/home.html', context)


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
    
    # Récupérer l'ID Free Fire stocké en session pour ce produit
    player_id_key = f'player_id_{product.id}'
    saved_player_id = request.session.get(player_id_key, '')
    
    # Produits similaires de la même catégorie
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk).select_related('category')[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'is_redeem_product': product.is_redeem_product,
        'saved_player_id': saved_player_id,  # Ajouté
    }
    return render(request, 'store/product_detail.html', context)


def contact(request):
    """Page de contact avec envoi d'email"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', 'Non renseigné')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Envoyer l'email
        full_message = f"""
Nouveau message de contact - KOITA_STORE

Nom: {name}
Email: {email}
Téléphone: {phone}
Sujet: {subject}

Message:
{message}

---
Cet email a été envoyé depuis le formulaire de contact de KOITA_STORE
        """
        
        try:
            send_mail(
                subject=f"📧 Contact KOITA_STORE: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['koitastore@gmail.com'],  # Votre email
                fail_silently=False,
            )
            messages.success(request, '✅ Votre message a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.')
        except Exception as e:
            messages.error(request, f'❌ Erreur lors de l\'envoi du message: {str(e)}')
    
    return render(request, 'contact/contact.html')


@login_required
def process_order(request, order_id):
    """Traiter la commande après paiement - NOUVELLE FONCTION"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    for order_item in order.order_items.all():
        product = order_item.product
        
        # Vérifier si c'est un produit Free Fire Diamant (recharge automatique)
        if product.requires_free_fire_id():
            # Utiliser le script d'automatisation Shop2Game
            redeemer = Shop2GameRedeemer()
            success, message = redeemer.redeem_diamonds(
                free_fire_id=order.free_fire_id,
                redeem_code=product.redeem_code
            )
            
            if success:
                # Marquer le code comme utilisé
                product.redeem_code_used = True
                product.save()
                
                # Créer une notification de succès
                Notification.objects.create(
                    user=request.user,
                    notification_type='redeem',
                    title='✅ Recharge Free Fire Réussie',
                    message=f'Vos {product.name} ont été ajoutés à votre compte Free Fire (ID: {order.free_fire_id})',
                    redeem_code=product.redeem_code,
                    order=order
                )
                
                logger.info(f"Recharge automatique réussie pour {request.user.username}")
                
            else:
                # Si l'automatisation échoue, envoyer le code manuellement
                Notification.objects.create(
                    user=request.user,
                    notification_type='redeem',
                    title='🎁 Code REDEEM Free Fire',
                    message=f'Voici votre code REDEEM pour {product.name}. Utilisez-le sur shop2game.com',
                    redeem_code=product.redeem_code,
                    order=order
                )
                
                logger.warning(f"Recharge automatique échouée, envoi manuel pour {request.user.username}")
        
        # Pour les codes diamants (envoi simple du code)
        elif 'code diamant' in product.category.name.lower() and product.is_redeem_product:
            Notification.objects.create(
                user=request.user,
                notification_type='redeem', 
                title='🎁 Code Diamant Free Fire',
                message=f'Voici votre code REDEEM pour {product.name}',
                redeem_code=product.redeem_code,
                order=order
            )
            
            # Marquer le code comme utilisé
            product.redeem_code_used = True
            product.save()
    
    # Marquer la commande comme complétée
    order.status = 'completed'
    order.save()
    
    return redirect('cart:order_success', order_id=order.id)


def get_cart_items(request):
    """Fonction utilitaire pour récupérer les items du panier"""
    # Cette fonction simule la récupération des items du panier
    # À adapter selon votre implémentation du panier
    if hasattr(request, 'cart_items'):
        return request.cart_items
    return []


def checkout(request):
    """Vue checkout mise à jour avec ID Free Fire"""
    cart_items = get_cart_items(request)
    
    # Vérifier si un ID Free Fire est requis
    requires_free_fire_id = any(
        item.product.requires_free_fire_id() for item in cart_items
    )
    
    if request.method == 'POST':
        # Traitement du formulaire de checkout
        free_fire_id = request.POST.get('free_fire_id', '').strip()
        payment_method = request.POST.get('payment_method', 'wave')
        
        # Validation
        if requires_free_fire_id and not free_fire_id:
            messages.error(request, '❌ L\'ID Free Fire est requis pour les recharges automatiques.')
            return render(request, 'cart/checkout.html', {
                'cart_items': cart_items,
                'requires_free_fire_id': requires_free_fire_id,
                'free_fire_id': free_fire_id
            })
        
        # Créer la commande
        try:
            total_amount = sum(item.total_price() for item in cart_items)
            
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                free_fire_id=free_fire_id if requires_free_fire_id else '',
                status='pending'
            )
            
            # Créer les OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    redeem_code=item.product.redeem_code if item.product.is_redeem_product else ''
                )
            
            # Rediriger vers le traitement de la commande
            return redirect('store:process_order', order_id=order.id)
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de commande: {str(e)}")
            messages.error(request, '❌ Erreur lors de la création de la commande.')
    
    context = {
        'cart_items': cart_items,
        'requires_free_fire_id': requires_free_fire_id,
    }
    return render(request, 'cart/checkout.html', context)