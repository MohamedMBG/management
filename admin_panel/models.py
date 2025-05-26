from django.db import models
from django.contrib.auth.models import User
from client_panel.models import Client



class Administrateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Administrateur: {self.user.get_full_name() or self.user.username}"



class Fournisseur(models.Model):
    nom = models.CharField(max_length=50)
    telephone = models.CharField("Téléphone", max_length=20)
    email = models.EmailField("E-Mail", blank=True)
    adresse = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom} - {self.telephone}"


class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix_unitaire = models.DecimalField("Prix Unitaire", max_digits=8, decimal_places=2)
    quantite = models.IntegerField("Quantité")
    alert_quantite = models.PositiveIntegerField(
        "Alert Quantité",
        help_text="Seuil pour la notification de stock faible."
    )
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    image = models.ImageField(
        "Product Image",
        upload_to='products/',
        blank=True,
        null=True,
        default='products/default.png'
    )

    def __str__(self):
        return f"{self.designation} ({self.quantite}) - Fournisseur: {self.fournisseur.nom}"

    def is_below_alert_level(self):
        return self.quantite <= self.alert_quantite

class Achat(models.Model):
    quantite = models.IntegerField("Quantité")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Date d'achat", auto_now_add=True)

    def __str__(self):
        return f"Achat de {self.quantite} x {self.produit.designation} par {self.client}"