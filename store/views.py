from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    """Page d'accueil avec tous les produits"""
    products = Product.objects.filter(is_active=True)
    return render(request, 'store/home.html', {'products': products})

def recharges(request):
    """Page des recharges uniquement"""
    products = Product.objects.filter(category='recharge', is_active=True)
    return render(request, 'store/recharges.html', {'products': products})

def accounts_for_sale(request):
    """Page des comptes à vendre"""
    products = Product.objects.filter(category='account', is_active=True)
    return render(request, 'store/accounts.html', {'products': products})

def product_detail(request, pk):
    """Page de détail d'un produit"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def contact(request):
    """Page de contact"""
    return render(request, 'contact/contact.html')