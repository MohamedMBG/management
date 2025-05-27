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

    # Fournisseurs
    path('fournisseurs/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/ajouter/', views.fournisseur_add, name='add_fournisseur'),

    # Superviseurs (newly added)
    path('superviseurs/', views.superviseur_list, name='superviseur_list'),
    path('superviseurs/ajouter/', views.superviseur_add, name='add_superviseur'),
    path('superviseurs/modifier/<int:pk>/', views.superviseur_edit, name='edit_superviseur'),
    path('superviseurs/supprimer/<int:pk>/', views.superviseur_delete, name='delete_superviseur'),

    # Achats
    path('achats/', views.achats, name='achats'),
]