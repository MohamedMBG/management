# admin_panel/utils.py
from django.core.mail import send_mail
from django.conf import settings


def send_stock_alert(produit):
    if produit.is_below_alert_level() and produit.fournisseur.email:
        subject = f'Alerte Stock: {produit.designation}'
        message = (f"Le produit {produit.designation} a atteint son niveau d'alerte.\n"
                   f"Quantité actuelle: {produit.quantite}\n"
                   f"Niveau d'alerte: {produit.alert_quantite}\n\n"
                   f"Veuillez approvisionner ce produit.")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [produit.fournisseur.email],
            fail_silently=True,
        )
        return True
    return False