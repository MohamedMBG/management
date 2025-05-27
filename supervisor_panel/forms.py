from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Superviseur

class SuperviseurCreationForm(UserCreationForm):
    telephone = forms.CharField(max_length=20, required=True)
    adresse = forms.CharField(max_length=255, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Ensure email is saved
        if commit:
            user.save()
            Superviseur.objects.create(
                user=user,
                telephone=self.cleaned_data['telephone'],
                adresse=self.cleaned_data['adresse']
            )
        return user