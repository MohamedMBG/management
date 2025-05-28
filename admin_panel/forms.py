# admin_panel/forms.py
from django import forms
from .models import Produit, Fournisseur, Achat
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

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['produit', 'client', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'produit': 'Produit',
            'client': 'Client',
            'quantite': 'Quantité'
        }