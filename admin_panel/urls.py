# admin_panel/urls.py
from django.urls import path
from django.views.generic import RedirectView

from . import views

# Define the app_name for namespacing
app_name = 'admin_panel'

urlpatterns = [
    # Authentication routes
    path('login/', views.login_View, name='login'),
    
    # Dashboard route
    path('', views.dashboard_view, name='admin_dashboard'),
    path('produits/', views.produits_view, name='produits')

    # Optional: Add a default redirect within the admin_panel if needed
    # path('', RedirectView.as_view(url='login/', permanent=False)),
]

