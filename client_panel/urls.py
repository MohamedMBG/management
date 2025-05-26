from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup_View, name='signup'), # Ajoutez les chemins nécessaires
    #path('signin/', views.signin_View, name='signin'), # Ajoutez les chemins nécessaires
    path('signin/', views.signin_View, name='client_signin'),
    #path('dashboard/', views.dashboard_View, name='some_dashboard'),
    path('dashboard/', views.client_dashboard, name='some_dashboard'),
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('logout/', views.signout_View, name='client_logout'),
    # Product URLs
    path('products/', views.client_products, name='client_products'),
    path('purchase/<int:product_id>/', views.make_purchase, name='make_purchase'),

    # Purchase History URLs
    path('purchases/', views.client_achats, name='client_achats'),
]
