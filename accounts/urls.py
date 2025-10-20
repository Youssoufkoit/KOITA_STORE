from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # ============================================
    # AUTHENTIFICATION
    # ============================================
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # ============================================
    # PROFIL
    # ============================================
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # ============================================
    # MISE À JOUR DU PROFIL
    # ============================================
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/avatar/', views.update_avatar, name='update_avatar'),
    path('profile/password/', views.change_password, name='change_password'),
    path('profile/settings/', views.update_settings, name='update_settings'),
    
    # ============================================
    # SUPPRESSION DE COMPTE
    # ============================================
    path('delete/', views.delete_account, name='delete_account'),
    
    # ============================================
    # HISTORIQUE DES COMMANDES
    # ============================================
    path('orders/', views.order_history, name='order_history'),
    
    # ============================================
    # VÉRIFICATIONS AJAX (OPTIONNELLES)
    # ============================================
    path('check-username/', views.check_username_availability, name='check_username'),
    path('check-email/', views.check_email_availability, name='check_email'),
    
    # ============================================
    # VUE DE TEST (À SUPPRIMER EN PRODUCTION)
    # ============================================
    path('test-profile/', views.test_profile, name='test_profile'),
]
# accounts/urls.py - AJOUTER CES ROUTES

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # ... routes existantes ...
    
    # ============================================
    # NOTIFICATIONS
    # ============================================
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
]