# Importation des fonctions liées à l'authentification des utilisateurs
from django.contrib.auth import authenticate, login, logout

# Fonctions utiles pour gérer les vues (affichage, redirection, récupération d'objets)
from django.shortcuts import render, redirect, get_object_or_404
# Décorateur pour restreindre l'accès à une vue aux utilisateurs connectés
from django.contrib.auth.decorators import login_required
# Pour afficher des messages d'erreur ou de succès à l'utilisateur
from django.contrib import messages

from supervisor_panel.forms import SuperviseurCreationForm
# Importation des formulaires définis pour chaque modèle
from .forms import ProduitForm, FournisseurForm, SuperviseurForm, AchatForm
# Importation des modèles utilisés dans cette application
from .models import Produit, Fournisseur,Achat
# Importation d’un modèle depuis une autre application
from supervisor_panel.models import Superviseur  # Import depuis une autre app

""" Fonction utilitaire qui vérifie si l'utilisateur est un admin (membre du staff) """
def is_admin(user):
    return user.is_authenticated and user.is_staff


# Authentification
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Récupère le nom d'utilisateur du formulaire
        password = request.POST.get('password')  # Récupère le mot de passe du formulaire
        user = authenticate(request, username=username, password=password)  # Vérifie les identifiants

        # Si l'utilisateur est authentifié et est un admin
        if user and is_admin(user):
            login(request, user)  # Connecte l'utilisateur
            return redirect('admin_panel:admin_dashboard')  # Redirige vers le dashboard admin
        # Sinon, affiche un message d'erreur
        messages.error(request, 'Invalid credentials or not an admin')
    # Affiche la page de connexion
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('admin_panel:login')  # Redirige vers la page de connexion


# Tableau de bord (accès restreint aux utilisateurs connectés)
@login_required
def dashboard(request):
    return render(request, 'admin_panel/adminDashboard.html')


# Produits
@login_required
def produit_list(request):
    return render(request, 'admin_panel/produits.html', {
        'produits': Produit.objects.all()  # Récupère tous les produits
    })


@login_required
def produit_add(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)  # Remplit le formulaire avec les données POST
        if form.is_valid():
            form.save()  # Sauvegarde le produit en base de données
            messages.success(request, 'Product added successfully!')
            return redirect('admin_panel:produit_list')  # Redirige vers la liste
    else:
        form = ProduitForm()  # Formulaire vide
    return render(request, 'admin_panel/produit_form.html', {'form': form})

@login_required
def produit_edit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)  # Récupère le produit ou affiche 404
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès!')
            return redirect('admin_panel:produit_list')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'admin_panel/produit_form.html', {'form': form})


@login_required
def produit_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()  # Supprime le produit
        messages.success(request, 'Produit supprimé avec succès!')
        return redirect('admin_panel:produit_list')
    return render(request, 'admin_panel/produit_confirm_delete.html', {'produit': produit})

# Fournisseurs
@login_required
def fournisseur_list(request):
    return render(request, 'admin_panel/fournisseur.html', {
        'fournisseurs': Fournisseur.objects.all()
    })


@login_required
def fournisseur_add(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('admin_panel:fournisseur_list')
    else:
        form = FournisseurForm()
    return render(request, 'admin_panel/fournisseur_form.html', {'form': form})

@login_required
def fournisseur_edit(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fournisseur modifié avec succès!')
            return redirect('admin_panel:fournisseur_list')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'admin_panel/fournisseur_form.html', {'form': form})

@login_required
def fournisseur_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        fournisseur.delete()
        messages.success(request, 'Fournisseur supprimé avec succès!')
    return redirect('admin_panel:fournisseur_list')


# Superviseurs
@login_required
def superviseur_list(request):
    return render(request, 'admin_panel/superviseurs.html', {
        'superviseurs': Superviseur.objects.all()
    })


# Achats
# views.py
@login_required
def achats(request):
    achats = Achat.objects.select_related('produit', 'client').all()  # Récupère les achats avec leurs relations
    for achat in achats:
        achat.total = achat.quantite * achat.produit.prix_unitaire  # Calcule le total pour chaque achat
    return render(request, 'admin_panel/achats.html', {'achats': achats})

@login_required
def achat_create(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achat créé avec succès!')
            return redirect('admin_panel:achats')
    else:
        form = AchatForm()
    return render(request, 'admin_panel/achat_form.html', {'form': form})

@login_required
def achat_detail(request, pk):
    achat = get_object_or_404(Achat.objects.select_related('produit', 'client'), pk=pk)
    context = {
        'achat': achat,
        'montant_total': achat.produit.prix * achat.quantite  # Calcule le montant total
    }
    return render(request, 'admin_panel/achat_detail.html', context)


@login_required
def achat_update(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    if request.method == 'POST':
        form = AchatForm(request.POST, instance=achat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achat modifié avec succès!')
            return redirect('admin_panel:achat_detail', pk=achat.id)
    else:
        form = AchatForm(instance=achat)

    return render(request, 'admin_panel/achat_form.html', {
        'form': form,
        'title': 'Modifier Achat'
    })


@login_required
@login_required
def achat_delete(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    if request.method == 'POST':
        achat.delete()
        messages.success(request, 'Achat supprimé avec succès!')
    return redirect('admin_panel:achats')


""" ------------------------------------------------------ Superviseur views ------------------------------------------------------ """


@login_required
# Vue pour afficher les détails d'un superviseur
# Utilisée quand on veut voir le profil complet d'un superviseur
@login_required  # Décorateur Django - Limite l'accès aux utilisateurs connectés
def superviseur_detail(request, pk):
    # Renvoie une page avec les détails du superviseur
    # get_object_or_404 est une fonction utilitaire de Django qui:
    # - Cherche un superviseur avec l'ID (pk) donné
    # - Renvoie une erreur 404 si non trouvé
    return render(request, 'admin_panel/superviseur_detail.html', {
        'superviseur': get_object_or_404(Superviseur, pk=pk)
    })


# Vue pour ajouter un nouveau superviseur
# Utilisée quand on accède au formulaire d'ajout ou qu'on soumet le formulaire
def superviseur_add(request):
    # Crée le formulaire:
    # - request.POST or None: Prend les données du formulaire si méthode POST, sinon None
    # C'est une façon concise de gérer GET/POST
    form = SuperviseurCreationForm(request.POST or None)

    # Si la requête est POST ET que le formulaire est valide
    if request.method == 'POST' and form.is_valid():
        # Sauvegarde le nouveau superviseur (et crée l'utilisateur associé)
        form.save()
        # Ajoute un message de succès qui s'affichera à l'utilisateur
        messages.success(request, 'Superviseur créé avec succès!')
        # Redirige vers la liste des superviseurs
        # redirect() est une fonction utilitaire de Django
        return redirect('admin_panel:superviseur_list')

    # Si GET ou formulaire invalide: affiche le formulaire
    # render() est une fonction Django qui combine template + contexte
    return render(request, 'admin_panel/superviseur_form.html', {'form': form})


# Vue pour modifier un superviseur existant
# Utilisée pour afficher/modifier les infos d'un superviseur
@login_required  # Nécessite une connexion
def superviseur_edit(request, pk):
    # Récupère le superviseur ou 404
    superviseur = get_object_or_404(Superviseur, pk=pk)

    # Crée le formulaire avec:
    # - Données POST si existantes
    # - Instance du superviseur pour modification
    # - Valeurs initiales pour les champs liés à l'utilisateur
    form = SuperviseurForm(request.POST or None, instance=superviseur, initial={
        'username': superviseur.user.username,  # Champ du modèle User
        'first_name': superviseur.user.first_name,
        'last_name': superviseur.user.last_name,
        'email': superviseur.email,
    })

    # Si soumission valide
    if request.method == 'POST' and form.is_valid():
        form.save()  # Sauvegarde les modifications
        messages.success(request, 'Superviseur mis à jour!')
        return redirect('admin_panel:superviseur_list')

    # Affiche le formulaire de modification
    return render(request, 'admin_panel/superviseur_form.html', {
        'form': form,
        'title': 'Modifier le Superviseur'  # Titre contextuel pour le template
    })


# Vue pour supprimer un superviseur
# Utilisée pour confirmation et suppression effective
@login_required
def superviseur_delete(request, pk):
    # Récupère le superviseur
    superviseur = get_object_or_404(Superviseur, pk=pk)

    # Si confirmation reçue (méthode POST)
    if request.method == 'POST':
        superviseur.delete()  # Supprime le superviseur (et l'user via CASCADE)
        messages.success(request, 'Superviseur supprimé!')
        return redirect('admin_panel:superviseur_list')

    # Affiche la page de confirmation (pour les requêtes GET)
    return render(request, 'admin_panel/superviseur_confirm_delete.html', {
        'superviseur': superviseur
    })