from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SignUpForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404
from store.models import Notification, Order

# ============================================
# VUES D'AUTHENTIFICATION (EXISTANTES)
# ============================================

def login_view(request):
    """Vue de connexion"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie !')
                next_url = request.GET.get('next', 'store:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Identifiants incorrects')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue !')
            next_url = request.GET.get('next', 'store:home')
            return redirect(next_url)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Déconnexion réussie !')
    return redirect('store:home')


# ============================================
# VUES DE PROFIL (NOUVELLES)
# ============================================

@login_required
def profile_view(request):
    """Vue principale du profil utilisateur"""
    user = request.user
    profile = user.profile
    
    # Récupérer les commandes de l'utilisateur (CORRIGÉ)
    orders = []
    if hasattr(user, 'user_orders'):
        orders = user.user_orders.all().order_by('-created_at')[:10]  # CORRIGÉ: user_orders
    
    # Calculer les statistiques
    total_orders = profile.get_total_orders()
    total_spent = profile.get_total_spent()
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def update_profile(request):
    """Mise à jour des informations du profil"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Votre profil a été mis à jour avec succès!')
        else:
            messages.error(request, '❌ Erreur lors de la mise à jour du profil.')
    
    return redirect('accounts:profile')


@login_required
def update_avatar(request):
    """Mise à jour de la photo de profil"""
    if request.method == 'POST' and request.FILES.get('avatar'):
        try:
            profile = request.user.profile
            
            # Supprimer l'ancien avatar s'il existe
            if profile.avatar:
                profile.avatar.delete(save=False)
            
            # Sauvegarder le nouveau
            profile.avatar = request.FILES['avatar']
            profile.save()
            
            messages.success(request, '✅ Votre photo de profil a été mise à jour!')
        except Exception as e:
            messages.error(request, f'❌ Erreur lors de la mise à jour de la photo: {str(e)}')
    else:
        messages.error(request, '❌ Aucune image sélectionnée.')
    
    return redirect('accounts:profile')


@login_required
def change_password(request):
    """Changement de mot de passe"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important : mettre à jour la session pour éviter la déconnexion
            update_session_auth_hash(request, user)
            messages.success(request, '✅ Votre mot de passe a été modifié avec succès!')
        else:
            # Afficher les erreurs du formulaire
            for error in form.errors.values():
                messages.error(request, f'❌ {error}')
    
    return redirect('accounts:profile')


@login_required
def update_settings(request):
    """Mise à jour des paramètres utilisateur"""
    if request.method == 'POST':
        try:
            profile = request.user.profile
            
            # Mettre à jour les paramètres de notification
            profile.email_notifications = request.POST.get('email_notifications') == 'on'
            profile.order_notifications = request.POST.get('order_notifications') == 'on'
            
            # Mettre à jour les paramètres d'apparence
            profile.dark_mode = request.POST.get('dark_mode') == 'on'
            
            profile.save()
            messages.success(request, '✅ Vos paramètres ont été mis à jour!')
        except Exception as e:
            messages.error(request, f'❌ Erreur lors de la mise à jour: {str(e)}')
    
    return redirect('accounts:profile')


@login_required
@require_POST
def delete_account(request):
    """Suppression du compte utilisateur"""
    try:
        user = request.user
        
        # Déconnecter l'utilisateur
        logout(request)
        
        # Supprimer le compte
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Votre compte a été supprimé avec succès.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors de la suppression du compte: {str(e)}'
        }, status=400)


# ============================================
# VUE D'ÉDITION DE PROFIL (ALTERNATIVE)
# ============================================

@login_required
def edit_profile(request):
    """Vue d'édition du profil (page séparée alternative)"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Profil mis à jour avec succès!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)


# ============================================
# VUES UTILITAIRES (OPTIONNELLES)
# ============================================

@login_required
def order_history(request):
    """Vue pour l'historique complet des commandes"""
    orders = []
    if hasattr(request.user, 'user_orders'):  # CORRIGÉ: user_orders
        orders = request.user.user_orders.all().order_by('-created_at')  # CORRIGÉ: user_orders
    
    # Filtrer par statut si demandé
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
    }
    return render(request, 'accounts/order_history.html', context)


@login_required
def check_username_availability(request):
    """Vérifier si un nom d'utilisateur est disponible (AJAX)"""
    username = request.GET.get('username', '')
    
    if not username:
        return JsonResponse({'available': False, 'message': 'Nom d\'utilisateur vide'})
    
    # Vérifier si le username est pris (sauf pour l'utilisateur actuel)
    from django.contrib.auth.models import User
    is_available = not User.objects.exclude(id=request.user.id).filter(username=username).exists()
    
    return JsonResponse({
        'available': is_available,
        'message': 'Disponible' if is_available else 'Déjà pris'
    })


@login_required
def check_email_availability(request):
    """Vérifier si un email est disponible (AJAX)"""
    email = request.GET.get('email', '')
    
    if not email:
        return JsonResponse({'available': False, 'message': 'Email vide'})
    
    # Vérifier si l'email est pris (sauf pour l'utilisateur actuel)
    from django.contrib.auth.models import User
    is_available = not User.objects.exclude(id=request.user.id).filter(email=email).exists()
    
    return JsonResponse({
        'available': is_available,
        'message': 'Disponible' if is_available else 'Déjà utilisé'
    })


# ============================================
# VUE DE TEST (À SUPPRIMER EN PRODUCTION)
# ============================================

@login_required
def test_profile(request):
    """Vue de test pour vérifier que le profil existe"""
    user = request.user
    
    # Créer le profil s'il n'existe pas
    if not hasattr(user, 'profile'):
        from .models import Profile
        Profile.objects.create(user=user)
        messages.info(request, 'Profil créé automatiquement')
    
    context = {
        'has_profile': hasattr(user, 'profile'),
        'profile': user.profile if hasattr(user, 'profile') else None,
    }
    
    return render(request, 'accounts/test_profile.html', context)


# ============================================
# VUES DE NOTIFICATIONS
# ============================================

@login_required
def notifications_view(request):
    """Vue pour afficher toutes les notifications"""
    notifications = request.user.user_notifications.all().order_by('-created_at')  # CORRIGÉ: user_notifications
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'accounts/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Marquer une notification comme lue"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('accounts:notifications')


@login_required
def mark_all_notifications_read(request):
    """Marquer toutes les notifications comme lues"""
    request.user.user_notifications.filter(is_read=False).update(is_read=True)  # CORRIGÉ: user_notifications
    messages.success(request, '✅ Toutes les notifications ont été marquées comme lues')
    return redirect('accounts:notifications')


@login_required
def delete_notification(request, notification_id):
    """Supprimer une notification"""
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.delete()
        messages.success(request, '✅ Notification supprimée')
    return redirect('accounts:notifications')