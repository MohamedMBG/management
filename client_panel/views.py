from django.contrib.auth import login, logout  # Fonction intégrée Django pour connecter/déconnecter un utilisateur
from django.contrib.auth.decorators import login_required  # Décorateur Django qui exige que l'utilisateur soit connecté
from django.db.models import Sum  # Fonction intégrée Django pour faire la somme dans des requêtes ORM
from django.shortcuts import render, redirect, get_object_or_404  # Fonctions Django pour rendre un template, rediriger ou obtenir un objet ou afficher 404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Formulaires préconstruits de Django pour l'inscription et la connexion
from django.contrib.auth.models import User, Group  # Modèles intégrés de Django pour gérer les utilisateurs et les groupes
from django.contrib import messages  # Système intégré de Django pour afficher des messages à l'utilisateur

from admin_panel.models import Achat, Produit
from client_panel.models import Client

"""""
-----------------------------------------------------------------------------------------------------------------------------------------
Fonction: signup_View
Processus: Cette fonction gère la création d'un compte client.
Elle est utilisée lorsqu'un utilisateur soumet le formulaire d'inscription.
Elle crée un utilisateur (via UserCreationForm), l'associe au groupe "client",
puis crée un objet Client lié à cet utilisateur.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

def signup_View(request):
    # Si la requête est de type POST, cela signifie que l'utilisateur a soumis le formulaire
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Formulaire intégré de Django pour créer un utilisateur
        role = request.POST.get('role')  # Récupère le rôle choisi dans le formulaire (doit être "client")
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')

        # Vérifie que le formulaire est valide et que le rôle est bien "client"
        if form.is_valid() and role == 'client':
            user = form.save(commit=False)  # Crée l'utilisateur sans l'enregistrer tout de suite en base de données
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()  # Enregistre l'utilisateur avec les données supplémentaires

            # Ajoute l'utilisateur au groupe "client" (Group est un modèle intégré Django)
            user.groups.add(Group.objects.get(name='client'))

            # Crée un profil Client associé à cet utilisateur
            Client.objects.create(
                user=user,
                email=user.email,
                telephone=request.POST.get('telephone'),
                adresse=request.POST.get('adresse')
            )

            login(request, user)  # Fonction intégrée Django pour connecter automatiquement l'utilisateur
            messages.success(request, "Client account created successfully.")  # Message succès (via messages framework de Django)
            return redirect('client_signin')  # Redirige vers la page de connexion
        else:
            messages.error(request, "Please complete the form correctly.")  # Message d'erreur si invalidité
    else:
        form = UserCreationForm()  # Si ce n'est pas une requête POST, on affiche un formulaire vide

    return render(request, 'client_panel/signup.html', {'form': form})  # Rend le formulaire dans la page HTML


"""
-----------------------------------------------------------------------------------------------------------------------------------------
Fonction: signin_View
Processus: Gère la connexion des utilisateurs clients.
Elle utilise AuthenticationForm (formulaire intégré Django)
pour valider les identifiants et connecter l'utilisateur.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

def signin_View(request):
    form = AuthenticationForm(request, data=request.POST or None)  # Formulaire intégré Django pour se connecter
    if request.method == 'POST' and form.is_valid():  # Vérifie que c'est un POST et que les infos sont valides
        login(request, form.get_user())  # Fonction intégrée Django pour connecter l'utilisateur
        return redirect('some_dashboard')  # Redirige vers un tableau de bord
    return render(request, 'client_panel/signin.html', {'form': form})  # Affiche le formulaire de connexion


"""
-----------------------------------------------------------------------------------------------------------------------------------------
Fonction: signout_View
Processus: Déconnecte l'utilisateur et le redirige vers la page de connexion.
Utilise la fonction logout() fournie par Django.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
def signout_View(request):
    logout(request)  # Fonction intégrée Django pour déconnecter l'utilisateur
    messages.success(request, "Vous avez été déconnecté(e) avec succès.")  # Affiche un message de succès
    return redirect('client_signin')  # Redirige vers la page de connexion


"""
-----------------------------------------------------------------------------------------------------------------------------------------
Fonction: client_dashboard
Processus: Affiche le tableau de bord du client connecté.
Utilise les fonctions ORM intégrées de Django pour récupérer et agréger les données d'achat.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
@login_required  # Décorateur Django qui exige que l'utilisateur soit connecté

def client_dashboard(request):
    client = get_object_or_404(Client, user=request.user)  # Fonction Django pour récupérer ou afficher une erreur 404

    purchases = Achat.objects.filter(client=client)  # ORM Django : récupère tous les achats de ce client
    total_purchases = purchases.count()  # Compte le nombre total d'achats
    recent_orders = purchases.order_by('-created_at')[:5]  # Trie les achats par date descendante, prend les 5 premiers

    total_spent_result = purchases.aggregate(
        total_spent=Sum('produit__prix_unitaire')  # Fonction agrégée intégrée pour la somme
    )
    total_spent = total_spent_result['total_spent'] or 0  # Si aucun achat, met 0

    return render(request, 'client_panel/dashboard.html', {
        'client': client,
        'recent_orders': recent_orders,
        'total_purchases': total_purchases,
        'total_spent': total_spent,
        'active_orders': purchases.filter(status='processing').count() if hasattr(Achat, 'status') else 0
    })


"""
-----------------------------------------------------------------------------------------------------------------------------------------
Fonction: client_products
Processus: Affiche tous les produits en stock pour que le client puisse les consulter.
Utilise le moteur ORM de Django pour filtrer les produits.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
@login_required
def client_products(request):
    produits = Produit.objects.filter(quantite__gt=0)  # ORM Django : filtre les produits dont la quantité est > 0
    return render(request, 'client_panel/produits.html', {'produits': produits})  # Affiche les produits


"""
-----------------------------------------------------------------------------------------------------------------------------------------
Fonction: make_purchase
Processus: Permet à un client de faire un achat d'un produit donné.
Vérifie la quantité en stock, crée l'achat via ORM Django, et met à jour le stock.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
@login_required
def make_purchase(request, product_id):
    if request.method == 'POST':
        produit = get_object_or_404(Produit, pk=product_id)  # Récupère un produit ou affiche une 404 si inexistant
        quantity = int(request.POST.get('quantity', 1))  # Récupère la quantité, valeur par défaut = 1
        client = get_object_or_404(Client, user=request.user)  # Récupère le client lié à l'utilisateur connecté

        if quantity <= 0:
            messages.error(request, "Invalid quantity")  # Message d'erreur
            return redirect('client_products')  # Redirige vers la liste des produits

        if produit.quantite < quantity:
            messages.error(request, "Not enough stock available")  # Pas assez de stock
            return redirect('client_products')

        Achat.objects.create(
            quantite=quantity,
            client=client,
            produit=produit
        )  # Crée un nouvel objet Achat via ORM Django

        produit.quantite -= quantity  # Réduit le stock du produit
        produit.save()  # Sauvegarde les modifications dans la base

        messages.success(request, f"Successfully purchased {quantity} x {produit.designation}")
        return redirect('client_achats')  # Redirige vers l'historique d'achats

    return redirect('client_products')  # Si ce n'est pas POST, redirige vers les produits


"""
-----------------------------------------------------------------------------------------------------------------------------------------
Fonction: client_achats
Processus: Affiche l'historique des achats pour le client connecté.
Utilise ORM Django pour récupérer les achats triés par date.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
@login_required
def client_achats(request):
    client = get_object_or_404(Client, user=request.user)  # Récupère le client connecté ou affiche 404
    achats = Achat.objects.filter(client=client).order_by('-created_at')  # Trie les achats les plus récents en premier
    return render(request, 'client_panel/achats.html', {'achats': achats})  # Affiche l'historique d'achats