from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_panel.forms import ProduitForm, FournisseurForm, AchatForm, SuperviseurForm
from admin_panel.models import Produit, Fournisseur, Achat
from admin_panel.utility import send_stock_alert
from supervisor_panel.forms import SuperviseurCreationForm
from supervisor_panel.models import Superviseur

# === FONCTION UTILITAIRE ===

def is_admin(user):
    """ Vérifie si l'utilisateur est administrateur.
    Args: user: L'objet utilisateur à vérifier
    Returns: bool: True si l'utilisateur est authentifié et est un membre du staff, False sinon"""
    return user.is_authenticated and user.is_staff


# ===== FONCTIONS D'AUTHENTIFICATION =====

def login_view(request):
    """ Vue pour la page de connexion.
    Args: request: L'objet requête HTTP envoyé par le navigateur
    Returns:
        Une redirection vers le tableau de bord si connexion réussie, sinon affiche la page de connexion """
    # Vérifie si la méthode HTTP est POST (formulaire soumis par l'utilisateur)
    if request.method == 'POST':
        # authenticate est une fonction prédéfinie de Django qui vérifie les identifiants
        # request.POST est un dictionnaire qui contient les données du formulaire soumis
        user = authenticate(
            username=request.POST['username'],# request.POST['username'] récupère la valeur du champ 'username' du formulaire
            password=request.POST['password']# request.POST['password'] récupère la valeur du champ 'password' du formulaire
        )

        if user and is_admin(user): # Vérifie si l'authentification a réussi (user n'est pas None) et si l'utilisateur est admin
            # login est une fonction prédéfinie de Django qui crée une session pour l'utilisateur
            # Elle prend deux paramètres: la requête et l'utilisateur à connecter
            login(request, user)
            return redirect('admin_panel:admin_dashboard')

        messages.error(request, 'Identifiants invalides ou non admin')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('admin_panel:login')

# ===== TABLEAU DE BORD =====
# Protection de la vue - accessible uniquement aux utilisateurs connectés
@login_required
def dashboard(request):
    context = {
        'produits_count': Produit.objects.count(),
        'fournisseurs_count': Fournisseur.objects.count(),
        'achats_count': Achat.objects.count(),
        'superviseurs_count': Superviseur.objects.count(),
        'derniers_produits': Produit.objects.order_by('-id')[:4],
        'derniers_achats': Achat.objects.select_related('produit').order_by('-created_at')[:4],
        'user': request.user
    }
    return render(request, 'admin_panel/adminDashboard.html', context)

# ===== GESTION DES PRODUITS (CRUD) =====
@login_required
def produit_list(request):
    return render(request, 'admin_panel/produits.html', {'produits': Produit.objects.all()})


@login_required
def produit_manage(request, pk=None):
    """ Vue pour ajouter ou modifier un produit.

    Parametres :
        request: L'objet requête HTTP
        pk: Clé primaire du produit (None pour un nouveau produit)
    Returns:
        Le formulaire de produit puis une redirection vers la liste des produits
    """
    # Si la cle primere "pk" existe (modification), récupère le produit, sinon None (création)
    # get_object_or_404 est une fonction prédéfinie qui récupère un objet ou renvoie une erreur 404 si non trouvé
    produit = get_object_or_404(Produit, pk=pk) if pk else None

    # Crée un formulaire avec les données existantes si modification, ou vide si création
    # request.POST contient les données du formulaire soumis s'il existe, sinon None"
    # request.FILES contient les fichiers uploadés (pour l'image du produit)
    # instance=produit associe le formulaire à l'instance existante (si modification)
    form = ProduitForm(request.POST or None, request.FILES or None, instance=produit)

    # Vérifie si le formulaire a été soumis (POST) et s'il est valide
    if request.method == 'POST' and form.is_valid():
        # form.save() sauvegarde les données du formulaire dans la base de données
        # et renvoie l'instance du modèle sauvegardée
        produit = form.save()

        # Vérifie si le stock est bas et si un fournisseur est associé
        # is_below_alert_level() est une méthode personnalisée définie dans le modèle Produit
        if produit.is_below_alert_level() and produit.fournisseur:
            # Envoie une alerte au fournisseur quand la quantite du produit <= la quantite d'alert (fonction personnalisée)
            send_stock_alert(produit)

        # Ajoute un message de succès qui sera affiché à l'utilisateur
        messages.success(request, f'Produit {"modifié" if pk else "ajouté"}!')

        return redirect('admin_panel:produit_list')

    return render(request, 'admin_panel/produit_form.html', {'form': form})


@login_required
def produit_delete(request, pk):
    """ Vue pour supprimer un produit. """
    if request.method == 'POST':
        # Récupère le produit et le supprime immédiatement avec .delete()
        get_object_or_404(Produit, pk=pk).delete()
        messages.success(request, 'Produit supprimé!')
        return redirect('admin_panel:produit_list')


# ===== GESTION DES FOURNISSEURS (CRUD) =====

@login_required
def fournisseur_list(request):
    return render(request, 'admin_panel/fournisseur.html', {'fournisseurs': Fournisseur.objects.all()})


@login_required
def fournisseur_manage(request, pk=None):
    """ Vue pour ajouter ou modifier un fournisseur. """
    # Si pk existe (modification), récupère le fournisseur, sinon None (création)
    fournisseur = get_object_or_404(Fournisseur, pk=pk) if pk else None

    # Crée un formulaire avec les données existantes si modification, ou vide si création
    # Notez qu'ici il n'y a pas de request.FILES car ce formulaire ne gère pas de fichiers
    form = FournisseurForm(request.POST or None, instance=fournisseur)

    # Vérifie si le formulaire a été soumis (POST) et s'il est valide
    if request.method == 'POST' and form.is_valid():
        # Sauvegarde les données du formulaire dans la base de données
        form.save()

        # Ajoute un message de succès
        messages.success(request, f'Fournisseur {"modifié" if pk else "ajouté"}!')

        # Redirige vers la liste des fournisseurs après la sauvegarde
        return redirect('admin_panel:fournisseur_list')

    # Si méthode GET ou formulaire invalide, affiche le formulaire
    return render(request, 'admin_panel/fournisseur_form.html', {'form': form})


@login_required
def fournisseur_delete(request, pk):
    """
    Vue pour supprimer un fournisseur.

    Args:
        request: L'objet requête HTTP
        pk: Clé primaire du fournisseur à supprimer

    Returns:
        Une redirection vers la liste des fournisseurs
    """
    # Vérifie si la méthode est POST (confirmation de suppression)
    if request.method == 'POST':
        # Récupère le fournisseur et le supprime
        get_object_or_404(Fournisseur, pk=pk).delete()

        # Ajoute un message de confirmation
        messages.success(request, 'Fournisseur supprimé!')

        # Redirige vers la liste des fournisseurs après la suppression
        return redirect('admin_panel:fournisseur_list')
    # Si la méthode est GET, rien ne se passe (la vue attend une méthode POST)


# ===== GESTION DES ACHATS (CRUD) =====

@login_required
def achats(request):
    """
    Vue pour afficher la liste de tous les achats.

    Args:
        request: L'objet requête HTTP

    Returns:
        La page avec la liste des achats et le montant total
    """
    # select_related est une méthode prédéfinie qui optimise les requêtes en chargeant les relations en une seule requête
    # Ici, on charge les relations 'produit' et 'client' pour chaque achat, ce qui évite des requêtes supplémentaires
    achats = Achat.objects.select_related('produit', 'client').all()

    # Renvoie le template avec un contexte contenant les achats et le montant total
    return render(request, 'admin_panel/achats.html', {
        'achats': achats,
        # Calcule le montant total de tous les achats avec une compréhension de liste
        # Pour chaque achat, on multiplie la quantité par le prix unitaire du produit
        # sum() additionne tous ces montants
        'montant_total': sum(a.quantite * a.produit.prix_unitaire for a in achats)
    })


@login_required
def achat_detail(request, pk):
    """
    Vue détaillée d'un achat avec calculs.

    Args:
        request: L'objet requête HTTP
        pk: Clé primaire de l'achat

    Returns:
        La page de détail de l'achat
    """
    # Récupère l'achat avec ses relations (produit et client)
    # select_related optimise la requête en chargeant les relations en une seule fois
    achat = get_object_or_404(Achat.objects.select_related('produit', 'client'), pk=pk)

    # Prépare le contexte à passer au template
    context = {
        'achat': achat,
        # Calcule le montant total de cet achat (quantité × prix unitaire)
        'montant_total': achat.quantite * achat.produit.prix_unitaire
    }

    # Renvoie le template avec le contexte
    return render(request, 'admin_panel/achat_detail.html', context)


@login_required
def achat_manage(request, pk=None):
    """
    Vue pour ajouter ou modifier un achat.

    Args:
        request: L'objet requête HTTP
        pk: Clé primaire de l'achat (None pour un nouvel achat)

    Returns:
        Le formulaire d'achat ou une redirection vers le détail de l'achat
    """
    # Si pk existe (modification), récupère l'achat, sinon None (création)
    achat = get_object_or_404(Achat, pk=pk) if pk else None

    # Crée un formulaire avec les données existantes si modification, ou vide si création
    form = AchatForm(request.POST or None, instance=achat)

    # Vérifie si le formulaire a été soumis (POST) et s'il est valide
    if request.method == 'POST' and form.is_valid():
        # Sauvegarde les données du formulaire dans la base de données
        achat = form.save()

        # Récupère le produit associé à cet achat
        produit = achat.produit

        # Met à jour la quantité du produit (diminue le stock)
        produit.quantite -= achat.quantite

        # Sauvegarde les modifications du produit
        produit.save()

        # Vérifie si une alerte de stock doit être envoyée
        # send_stock_alert est une fonction utilitaire qui renvoie True si une alerte a été envoyée
        if send_stock_alert(produit):
            # Ajoute un message d'information qui sera affiché à l'utilisateur
            messages.info(request, f"Alerte envoyée à {produit.fournisseur.nom}")

        # Ajoute un message de succès
        messages.success(request, f'Achat {"modifié" if pk else "créé"}!')

        # Redirige vers la page de détail de l'achat
        # Si c'est un nouvel achat (pk=None), on utilise l'ID de l'instance créée (form.instance.pk)
        # Sinon, on utilise l'ID existant (pk)
        return redirect('admin_panel:achat_detail', pk=form.instance.pk if not pk else pk)

    # Si méthode GET ou formulaire invalide, affiche le formulaire
    return render(request, 'admin_panel/achat_form.html', {'form': form})


@login_required
def achat_delete(request, pk):
    """
    Vue pour supprimer un achat.

    Args:
        request: L'objet requête HTTP
        pk: Clé primaire de l'achat à supprimer

    Returns:
        Une redirection vers la liste des achats
    """
    # Vérifie si la méthode est POST (confirmation de suppression)
    if request.method == 'POST':
        # Récupère l'achat et le supprime
        get_object_or_404(Achat, pk=pk).delete()

        # Ajoute un message de confirmation
        messages.success(request, 'Achat supprimé!')

        # Redirige vers la liste des achats après la suppression
        return redirect('admin_panel:achats')
    # Si la méthode est GET, rien ne se passe (la vue attend une méthode POST)


# ===== GESTION DES SUPERVISEURS (CRUD) =====

@login_required
def superviseur_list(request):
    """
    Vue pour afficher la liste de tous les superviseurs.

    Args:
        request: L'objet requête HTTP

    Returns:
        La page avec la liste des superviseurs
    """
    # Renvoie le template avec un contexte contenant tous les superviseurs
    return render(request, 'admin_panel/superviseurs.html', {'superviseurs': Superviseur.objects.all()})


@login_required
def superviseur_detail(request, pk):
    """
    Vue détaillée d'un superviseur (lecture seule).

    Args:
        request: L'objet requête HTTP
        pk: Clé primaire du superviseur

    Returns:
        La page de détail du superviseur
    """
    # Récupère le superviseur avec sa relation utilisateur
    # select_related optimise la requête en chargeant la relation 'user' en une seule fois
    superviseur = get_object_or_404(Superviseur.objects.select_related('user'), pk=pk)

    # Renvoie le template avec le superviseur dans le contexte
    return render(request, 'admin_panel/superviseur_detail.html', {'superviseur': superviseur})


@login_required
def superviseur_manage(request, pk=None):
    """
    Vue pour ajouter ou modifier un superviseur.

    Args:
        request: L'objet requête HTTP
        pk: Clé primaire du superviseur (None pour un nouveau superviseur)

    Returns:
        Le formulaire de superviseur ou une redirection vers la liste des superviseurs
    """
    # Si pk existe (modification), récupère le superviseur, sinon None (création)
    superviseur = get_object_or_404(Superviseur, pk=pk) if pk else None

    # Choisit le formulaire approprié selon qu'il s'agit d'une création ou d'une modification
    # SuperviseurForm pour la modification, SuperviseurCreationForm pour la création
    form_class = SuperviseurForm if pk else SuperviseurCreationForm

    # Initialise le formulaire avec les données existantes ou vide
    # initial permet de préremplir certains champs du formulaire
    # Ici, on prérempli le champ 'email' avec l'email du superviseur si c'est une modification
    form = form_class(
        request.POST or None,
        instance=superviseur,
        initial={'email': superviseur.email} if pk else None
    )

    # Vérifie si le formulaire a été soumis (POST) et s'il est valide
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Superviseur {"modifié" if pk else "créé"}!')
        return redirect('admin_panel:superviseur_list')

    # Si méthode GET ou formulaire invalide, affiche le formulaire
    return render(request, 'admin_panel/superviseur_form.html', {'form': form})


@login_required
def superviseur_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Superviseur, pk=pk).delete()
        messages.success(request, 'Superviseur supprimé!')
        return redirect('admin_panel:superviseur_list')

    # Si méthode GET, affiche la page de confirmation de suppression
    # Cette vue a un comportement différent des autres vues de suppression:
    # elle affiche une page de confirmation si la méthode est GET
    return render(request, 'admin_panel/superviseur_confirm_delete.html',
                 {'superviseur': get_object_or_404(Superviseur, pk=pk)})