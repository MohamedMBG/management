from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.superviseur_login_view, name='login'),
    path('dashboard/', views.superviseur_dashboard_view, name='dashboard'),
    path('logout/', views.superviseur_logout_view, name='logout'),
    path('report/stock/', views.superviseur_report_view, name='stock_report'),  # Specific URL for stock report
]