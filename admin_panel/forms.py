# admin_panel/forms.py
from django import forms
from .models import Produit, Fournisseur
from supervisor_panel.models import Superviseur

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'
        widgets = {
            'date_expiration': forms.DateInput(attrs={'type': 'date'}),
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class SuperviseurForm(forms.ModelForm):
    class Meta:
        model = Superviseur
        fields = '__all__'