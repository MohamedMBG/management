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
    path('produits/ajouter/', views.produit_add, name='add_produit'),
    path('produits/modifier/<int:pk>/', views.produit_edit, name='edit_produit'),
    path('produits/supprimer/<int:pk>/', views.produit_delete, name='delete_produit'),  # Add this line

    # Fournisseurs
    path('fournisseurs/ajouter/', views.fournisseur_add, name='add_fournisseur'),
    path('fournisseurs/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/modifier/<int:pk>/', views.fournisseur_edit, name='edit_fournisseur'),
    path('fournisseurs/supprimer/<int:pk>/', views.fournisseur_delete, name='delete_fournisseur'),


    # Superviseurs (newly added)
    path('superviseurs/', views.superviseur_list, name='superviseur_list'),
    path('superviseurs/ajouter/', views.superviseur_add, name='add_superviseur'),
    path('superviseurs/modifier/<int:pk>/', views.superviseur_edit, name='edit_superviseur'),
    path('superviseurs/supprimer/<int:pk>/', views.superviseur_delete, name='delete_superviseur'),
    path('superviseurs/<int:pk>/', views.superviseur_detail, name='superviseur_detail'),
    # Achats
    path('achats/', views.achats, name='achats'),
    path('achats/ajouter/', views.achat_create, name='achat_create'),  # Add this line
    path('achats/<int:pk>/', views.achat_detail, name='achat_detail'),
    path('achats/modifier/<int:pk>/', views.achat_update, name='achat_update'),
    path('achats/supprimer/<int:pk>/', views.achat_delete, name='achat_delete'),
]