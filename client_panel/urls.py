from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup_View, name='signup'), # Ajoutez les chemins nécessaires
    #path('signin/', views.signin_View, name='signin'), # Ajoutez les chemins nécessaires
    path('signin/', views.signin_View, name='client_signin'),
    path('dashboard/', views.dashboard_View, name='some_dashboard'),
]
