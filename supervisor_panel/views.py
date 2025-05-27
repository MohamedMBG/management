from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse # Import HttpResponse for CSV
import csv # Import csv module
import json
import datetime # To timestamp the report filename

from .models import Superviseur
from admin_panel.models import Produit, Achat

def superviseur_login_view(request):
    if request.user.is_authenticated:
        try:
            Superviseur.objects.get(user=request.user)
            return redirect(reverse("supervisor_panel:dashboard"))
        except Superviseur.DoesNotExist:
            logout(request)
            return redirect(reverse("supervisor_panel:login"))

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    Superviseur.objects.get(user=user)
                    login(request, user)
                    return redirect(reverse("supervisor_panel:dashboard"))
                except Superviseur.DoesNotExist:
                    pass # Stay on login page, maybe add error message
            else:
                pass # Stay on login page, maybe add error message
    else:
        form = AuthenticationForm()
    return render(request, "supervisor_panel/supervisor_login.html", {"form": form})

@login_required
def superviseur_dashboard_view(request):
    try:
        Superviseur.objects.get(user=request.user)
        products = Produit.objects.all().order_by("designation")
        stock_labels = [p.designation for p in products]
        stock_data = [p.quantite for p in products]
        stock_alert_levels = [p.alert_quantite for p in products]

        sales_by_month = (
            Achat.objects
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total_quantity=Sum("quantite"))
            .order_by("month")
        )
        sales_labels = [sale["month"].strftime("%Y-%m") for sale in sales_by_month]
        sales_data = [sale["total_quantity"] for sale in sales_by_month]

        context = {
            "stock_labels": json.dumps(stock_labels),
            "stock_data": json.dumps(stock_data),
            "stock_alert_levels": json.dumps(stock_alert_levels),
            "sales_labels": json.dumps(sales_labels),
            "sales_data": json.dumps(sales_data),
        }
        return render(request, "supervisor_panel/supervisor_dashboard.html", context)
    except Superviseur.DoesNotExist:
        logout(request)
        return redirect(reverse("supervisor_panel:login"))

@login_required
def superviseur_logout_view(request):
    logout(request)
    return redirect(reverse("supervisor_panel:login"))

@login_required
def superviseur_report_view(request):
    try:
        Superviseur.objects.get(user=request.user)

        # Define the type of report (e.g., 'stock', 'sales') based on request or keep it simple for now
        # For simplicity, let's generate a stock report first.

        response = HttpResponse(
            content_type='text/csv/',
            headers={'Content-Disposition": f\'attachment; filename="stock_report_{datetime.date.today()}.csv"'}, # Dynamic filename
        )

        writer = csv.writer(response)
        # Write header row
        writer.writerow(["Designation", "Quantity", "Unit Price", "Alert Level", "Supplier"])

        # Write data rows
        products = Produit.objects.select_related("fournisseur").all()
        for product in products:
            writer.writerow([
                product.designation,
                product.quantite,
                product.prix_unitaire,
                product.alert_quantite,
                product.fournisseur.nom if product.fournisseur else "N/A",
            ])

        return response

    except Superviseur.DoesNotExist:
        logout(request)
        return redirect(reverse("supervisor_panel:login"))

