from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Produit  # Import the Produit model

def login_View(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            # Assuming login.html is in the root templates directory or admin_panel templates
            return render(request, 'admin_panel/login.html') 

        # Attempt to authenticate using username
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_panel:admin_dashboard')
        else:
            # Add error message for failed login
            messages.error(request, 'Invalid username or password.')
            return render(request, 'admin_panel/login.html')

    else:
        # Ensure the login template path is correct
        return render(request, 'admin_panel/login.html')

# Dashboard view using the existing template
def dashboard_view(request):
    # Basic access control: only authenticated staff/admins
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Please log in as an administrator.')
        # Redirect to the namespaced login view
        return redirect('admin_panel:login') 
    
    # Render the existing dashboard template
    context = {
        'username': request.user.username
    }
    return render(request, 'admin_panel/adminDashboard.html', context)

# Updated produits_view to fetch and display products
def produits_view(request):
    # Fetch all products from the database
    produits_list = Produit.objects.all()
    
    # Pass the products to the template context
    context = {
        'produits': produits_list,
        'username': request.user.username # Pass username for consistency if needed in template
    }
    return render(request, 'admin_panel/produits.html', context)

