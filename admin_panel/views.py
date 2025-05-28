from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_panel.forms import ProduitForm, FournisseurForm, AchatForm, SuperviseurForm
from admin_panel.models import Produit, Fournisseur, Achat
from admin_panel.utility import send_stock_alert
from supervisor_panel.forms import SuperviseurCreationForm
from supervisor_panel.models import Superviseur


def is_admin(user):
    """Vérifie si l'utilisateur est admin"""
    return user.is_authenticated and user.is_staff

# Authentification
def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and is_admin(user):
            login(request, user)
            return redirect('admin_panel:admin_dashboard')
        messages.error(request, 'Identifiants invalides ou non admin')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('admin_panel:login')

# Tableau de bord
@login_required
def dashboard(request):
    return render(request, 'admin_panel/adminDashboard.html')

# CRUD Produits
@login_required
def produit_list(request):
    return render(request, 'admin_panel/produits.html', {'produits': Produit.objects.all()})

@login_required
def produit_manage(request, pk=None):
    produit = get_object_or_404(Produit, pk=pk) if pk else None
    form = ProduitForm(request.POST or None, request.FILES or None, instance=produit)

    if request.method == 'POST' and form.is_valid():
        produit = form.save()

        if produit.is_below_alert_level() and produit.fournisseur:
            send_stock_alert(produit)
        messages.success(request, f'Produit {"modifié" if pk else "ajouté"}!')
        return redirect('admin_panel:produit_list')

    return render(request, 'admin_panel/produit_form.html', {'form': form})

@login_required
def produit_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Produit, pk=pk).delete()
        messages.success(request, 'Produit supprimé!')
    return redirect('admin_panel:produit_list')


# CRUD Fournisseurs
@login_required
def fournisseur_list(request):
    return render(request, 'admin_panel/fournisseur.html', {'fournisseurs': Fournisseur.objects.all()})
@login_required
def fournisseur_manage(request, pk=None):
    fournisseur = get_object_or_404(Fournisseur, pk=pk) if pk else None
    form = FournisseurForm(request.POST or None, instance=fournisseur)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Fournisseur {"modifié" if pk else "ajouté"}!')
        return redirect('admin_panel:fournisseur_list')

    return render(request, 'admin_panel/fournisseur_form.html', {'form': form})
@login_required
def fournisseur_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Fournisseur, pk=pk).delete()
        messages.success(request, 'Fournisseur supprimé!')
    return redirect('admin_panel:fournisseur_list')


# CRUD Achats
@login_required
def achats(request):
    achats = Achat.objects.select_related('produit', 'client').all()
    return render(request, 'admin_panel/achats.html', {
        'achats': achats,
        'montant_total': sum(a.quantite * a.produit.prix_unitaire for a in achats)
    })
@login_required
def achat_detail(request, pk):
    """Detailed view of a purchase with calculations"""
    achat = get_object_or_404(Achat.objects.select_related('produit', 'client'), pk=pk)
    context = {
        'achat': achat,
        'montant_total': achat.quantite * achat.produit.prix_unitaire
    }
    return render(request, 'admin_panel/achat_detail.html', context)
@login_required
def achat_manage(request, pk=None):
    achat = get_object_or_404(Achat, pk=pk) if pk else None
    form = AchatForm(request.POST or None, instance=achat)

    # if request.method == 'POST' and form.is_valid():
    #     form.save()
    #     messages.success(request, f'Achat {"modifié" if pk else "créé"}!')
    #     return redirect('admin_panel:achat_detail', pk=form.instance.pk if not pk else pk)


    if request.method == 'POST' and form.is_valid():
        achat = form.save()
        produit = achat.produit
        produit.quantite -= achat.quantite
        produit.save()
        if send_stock_alert(produit):  # Using the utility function
            messages.info(request, f"Alerte envoyée à {produit.fournisseur.nom}")
        messages.success(request, f'Achat {"modifié" if pk else "créé"}!')
        return redirect('admin_panel:achat_detail', pk=form.instance.pk if not pk else pk)

    return render(request, 'admin_panel/achat_form.html', {'form': form})


@login_required
def achat_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Achat, pk=pk).delete()
        messages.success(request, 'Achat supprimé!')
    return redirect('admin_panel:achats')


# CRUD Superviseurs
@login_required
def superviseur_list(request):
    return render(request, 'admin_panel/superviseurs.html', {'superviseurs': Superviseur.objects.all()})

@login_required
def superviseur_detail(request, pk):
    """View-only detail page for supervisors"""
    superviseur = get_object_or_404(Superviseur.objects.select_related('user'), pk=pk)
    return render(request, 'admin_panel/superviseur_detail.html', {'superviseur': superviseur})
@login_required
def superviseur_manage(request, pk=None):
    superviseur = get_object_or_404(Superviseur, pk=pk) if pk else None
    form_class = SuperviseurForm if pk else SuperviseurCreationForm

    form = form_class(request.POST or None, instance=superviseur,
                      initial={'email': superviseur.email} if pk else None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Superviseur {"modifié" if pk else "créé"}!')
        return redirect('admin_panel:superviseur_list')

    return render(request, 'admin_panel/superviseur_form.html', {'form': form})


@login_required
def superviseur_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Superviseur, pk=pk).delete()
        messages.success(request, 'Superviseur supprimé!')
        return redirect('admin_panel:superviseur_list')
    return render(request, 'admin_panel/superviseur_confirm_delete.html',
                  {'superviseur': get_object_or_404(Superviseur, pk=pk)})