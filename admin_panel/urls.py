# admin_panel/urls.py
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='admin_dashboard'),

    # Produits
    path('produits/', views.produit_list, name='produit_list'),
    path('produits/ajouter/', views.produit_manage, name='produit_create'),
    path('produits/modifier/<int:pk>/', views.produit_manage, name='produit_update'),
    path('produits/supprimer/<int:pk>/', views.produit_delete, name='produit_delete'),

    # Fournisseurs
    path('fournisseurs/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/ajouter/', views.fournisseur_manage, name='fournisseur_create'),
    path('fournisseurs/modifier/<int:pk>/', views.fournisseur_manage, name='fournisseur_update'),
    path('fournisseurs/supprimer/<int:pk>/', views.fournisseur_delete, name='fournisseur_delete'),

    # Superviseurs
    path('superviseurs/', views.superviseur_list, name='superviseur_list'),
    path('superviseurs/ajouter/', views.superviseur_manage, name='superviseur_create'),
    path('superviseurs/modifier/<int:pk>/', views.superviseur_manage, name='superviseur_update'),
    path('superviseurs/supprimer/<int:pk>/', views.superviseur_delete, name='superviseur_delete'),
    path('superviseurs/<int:pk>/', views.superviseur_detail, name='superviseur_detail'),

    # Achats
    path('achats/', views.achats, name='achats'),
    path('achats/ajouter/', views.achat_manage, name='achat_create'),
    path('achats/modifier/<int:pk>/', views.achat_manage, name='achat_update'),
    path('achats/<int:pk>/', views.achat_detail, name='achat_detail'),
    path('achats/supprimer/<int:pk>/', views.achat_delete, name='achat_delete'),
]