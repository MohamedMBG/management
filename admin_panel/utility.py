# admin_panel/utils.py
from django.core.mail import send_mail
from django.conf import settings

"""
Cette fonction on l'appelle quand un client effectue un achat, ou un admin ajoute un produit, elle va etre
trigger une fois le produit atteint sa seuil d'alert "alert_quantity", elle recoit la quantite du produit
et l'email de son fournisseur, puis elle lui envoi un email.
"""
def send_stock_alert(produit):
    #la fonction recoit le produit comme un parametre
    if produit.is_below_alert_level() and produit.fournisseur.email:
        #si la quantite de produit < alert_quantite et le fournisseur du produit a un email fait le suivant:
        subject = f'Alerte Stock: {produit.designation}'
        #le sujet de l'email
        message = (f"Le produit {produit.designation} a atteint son niveau d'alerte.\n"
                   f"Quantité actuelle: {produit.quantite}\n"
                   f"Niveau d'alerte: {produit.alert_quantite}\n\n"
                   f"Veuillez approvisionner ce produit.")
        #le contenu de l'email

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [produit.fournisseur.email], #le récepteur de l'email et le fournisseur de produit
            fail_silently=True,
        )
        return True
    return False