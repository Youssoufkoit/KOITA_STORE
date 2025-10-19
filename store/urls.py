from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('recharges/', views.recharges, name='recharges'),
    path('accounts-for-sale/', views.accounts_for_sale, name='accounts_for_sale'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
]