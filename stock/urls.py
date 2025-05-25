"""
URL configuration for stock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from admin_panel.views import login_View

urlpatterns = [
    path('admin/', admin.site.urls),
    #path of admin
    path('admin_panel/' , include(('admin_panel.urls' , 'admin_panel') , namespace='admin_panel')),
    path('', RedirectView.as_view(url='admin_panel/login/', permanent=False)),
    path('admin_panel/login/', login_View , name='login'),

    #paths de client
    #path('client_panel/' , include(('client_panel.urls' , 'client_panel') , namespace='client_panel')),


    #paths de superviseur
    #path('supervisor_panel/' , include(('supervisor_panel.urls' , 'supervisor_panel') , namespace='supervisor_panel')),
]
