# Importation des outils nécessaires depuis Django et Python
from django.shortcuts import render, redirect  # Pour afficher des pages et rediriger
from django.contrib.auth import authenticate, login, logout  # Pour gérer les connexions
from django.contrib.auth.forms import AuthenticationForm  # Formulaire de connexion prêt à l'emploi
from django.contrib.auth.decorators import login_required  # Pour protéger l'accès aux pages
from django.db.models import Sum  # Pour faire des sommes
from django.db.models.functions import TruncMonth  # Pour grouper par mois
from django.http import HttpResponse  # Pour renvoyer des réponses HTTP
import csv  # Pour générer des fichiers CSV
import json  # Pour formater des données en JSON
import datetime  # Pour manipuler les dates

# Importation des modèles (tables avec la base de données)
from .models import Superviseur  # Table des superviseurs
from admin_panel.models import Produit, Achat  # Tables des produits et achats


def check_supervisor(user):
    """
    Vérifie si l'utilisateur est un superviseur
    1 user.is_authenticated : vérifie si l'utilisateur est connecté
    2 Superviseur.objects.filter : vérifie si l'utilisateur est dans la table Superviseur
    """
    return user.is_authenticated and Superviseur.objects.filter(user=user).exists()


""" ##################################### Vue pour la page de connexion des superviseurs ##################################### """
def superviseur_login_view(request):
    # Si l'utilisateur est déjà connecté et superviseur, on le redirige
    if check_supervisor(request.user):
        return redirect("supervisor_panel:dashboard")

    # Sinon préparation du formulaire de connexion
    # - request.POST contient les données envoyées par le formulaire
    # - Si pas de données (premier accès), on crée un formulaire vide
    form = AuthenticationForm(request, data=request.POST or None)

    # Quand le formulaire est soumis (méthode POST) et valide
    if request.method == "POST" and form.is_valid():
        # On vérifie les identifiants
        user = authenticate(**form.cleaned_data)

        # Si les identifiants sont bons ET que c'est un superviseur
        if user and check_supervisor(user):
            login(request, user)  # On connecte l'utilisateur
            return redirect("supervisor_panel:dashboard")  # Redirection vers le tableau de bord

    # Sinon affichage de la page de connexion (avec le formulaire)
    return render(request, "supervisor_panel/supervisor_login.html", {"form": form})


""" ##################################### Vue pour le tableau de bord des superviseurs ##################################### """
@login_required  # Seulement pour utilisateurs connectés
def superviseur_dashboard_view(request):
    # Sécurité : si l'utilisateur n'est pas superviseur, on le déconnecte
    if not check_supervisor(request.user):
        logout(request)
        return redirect("supervisor_panel:login")

    # Récupération de tous les produits triés par nom
    products = Produit.objects.all().order_by("designation")

    # Calcul des ventes par mois
    sales_by_month = (
        Achat.objects
        .annotate(month=TruncMonth("created_at"))  # On groupe par mois
        .values("month")  # On ne garde que le mois
        .annotate(total_quantity=Sum("quantite"))  # On somme les quantités
        .order_by("month")  # Tri par mois
    )

    # Préparation des données pour les graphiques
    context = {
        # Noms des produits (pour les étiquettes du graphique)
        "stock_labels": json.dumps([p.designation for p in products]),
        # Quantités en stock (pour les données du graphique)
        "stock_data": json.dumps([p.quantite for p in products]),
        # Niveaux d'alerte (pour les seuils critiques)
        "stock_alert_levels": json.dumps([p.alert_quantite for p in products]),
        # Mois des ventes (format "AAAA-MM")
        "sales_labels": json.dumps([sale["month"].strftime("%Y-%m") for sale in sales_by_month]),
        # Quantités vendues par mois
        "sales_data": json.dumps([sale["total_quantity"] for sale in sales_by_month]),
    }
    # Affichage du tableau de bord avec les données préparées
    return render(request, "supervisor_panel/supervisor_dashboard.html", context)


""" ########################################## Vue pour déconnecter l'utilisateur ######################################### """
@login_required
def superviseur_logout_view(request):
    logout(request)  # On déconnecte
    return redirect("supervisor_panel:login")  # Retour à la page de connexion


""" ########################################## Vue pour générer un rapport CSV des stocks ######################################### """
@login_required
def superviseur_report_view(request):
    # Sécurité : vérification que c'est bien un superviseur
    if not check_supervisor(request.user):
        logout(request)
        return redirect("supervisor_panel:login")

    # Préparation d'une réponse HTTP de type CSV
    response = HttpResponse(content_type='text/csv')
    # Nom du fichier avec la date du jour
    response['Content-Disposition'] = f'attachment; filename="stock_report_{datetime.date.today()}.csv"'

    # Création du writer CSV
    writer = csv.writer(response)
    # Entêtes des colonnes
    writer.writerow(["Designation", "Quantity", "Unit Price", "Alert Level", "Supplier"])

    # Récupération de tous les produits avec leurs fournisseurs
    products = Produit.objects.select_related("fournisseur").all()
    # Écriture des données produit par produit
    writer.writerows([
        [
            p.designation,  # Nom du produit
            p.quantite,  # Quantité en stock
            p.prix_unitaire,  # Prix unitaire
            p.alert_quantite,  # Niveau d'alerte
            p.fournisseur.nom if p.fournisseur else "N/A",  # Nom du fournisseur ou "N/A"
        ] for p in products
    ])

    # Renvoi du fichier CSV généré
    return response