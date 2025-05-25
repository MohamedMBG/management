from django.contrib import admin

from admin_panel.models import Administrateur, Produit, Achat

# Register your models here.
admin.site.register(Administrateur)
admin.site.register(Produit)
admin.site.register(Achat)
