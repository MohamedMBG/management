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
        fields = '__all__'
        widgets = {
            'date_achat': forms.DateInput(attrs={'type': 'date'}),
            'date_livraison': forms.DateInput(attrs={'type': 'date'}),
        }