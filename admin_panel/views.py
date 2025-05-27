from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ProduitForm, FournisseurForm, SuperviseurForm
from .models import Produit, Fournisseur,Achat
from supervisor_panel.models import Superviseur  # Import from the other app



# Helper function to check admin status
def is_admin(user):
    return user.is_authenticated and user.is_staff


# Authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and is_admin(user):
            login(request, user)
            return redirect('admin_panel:admin_dashboard')
        messages.error(request, 'Invalid credentials or not an admin')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('admin_panel:login')


# Dashboard
@login_required
def dashboard(request):
    return render(request, 'admin_panel/adminDashboard.html')


# Produits
@login_required
def produit_list(request):
    return render(request, 'admin_panel/produits.html', {
        'produits': Produit.objects.all()
    })


@login_required
def produit_add(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_panel:produit_list')
    else:
        form = ProduitForm()
    return render(request, 'admin_panel/produit_form.html', {'form': form})


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


# Superviseurs
@login_required
def superviseur_list(request):
    return render(request, 'admin_panel/superviseurs.html', {
        'superviseurs': Superviseur.objects.all()
    })


# Achats
@login_required
def achats(request):
    return render(request, 'admin_panel/achats.html', {
        'total_amount': Achat.objects.aggregate(Sum('montant'))['montant__sum'] or 0,
        'purchase_count': Achat.objects.count()
    })


@login_required
def superviseur_add(request):
    if request.method == 'POST':
        form = SuperviseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Superviseur ajouté avec succès!')
            return redirect('admin_panel:superviseur_list')
    else:
        form = SuperviseurForm()
    return render(request, 'admin_panel/superviseur_form.html', {'form': form})

@login_required
def superviseur_edit(request, pk):
    superviseur = get_object_or_404(Superviseur, pk=pk)
    if request.method == 'POST':
        form = SuperviseurForm(request.POST, instance=superviseur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Superviseur mis à jour!')
            return redirect('admin_panel:superviseur_list')
    else:
        form = SuperviseurForm(instance=superviseur)
    return render(request, 'admin_panel/superviseur_form.html', {'form': form})

@login_required
def superviseur_delete(request, pk):
    superviseur = get_object_or_404(Superviseur, pk=pk)
    if request.method == 'POST':
        superviseur.delete()
        messages.success(request, 'Superviseur supprimé!')
        return redirect('admin_panel:superviseur_list')
    return render(request, 'admin_panel/superviseur_confirm_delete.html', {'superviseur': superviseur})