from django.contrib import admin

from admin_panel.models import Administrateur, Produit, Achat, Fournisseur

# Register your models here.
admin.site.register(Administrateur)
admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(Achat)
