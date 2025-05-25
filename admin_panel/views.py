from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_View(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'login.html')

        # Attempt to authenticate using username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Check if the user is an admin (staff or superuser)
            if user.is_staff or user.is_superuser:
                # Redirect to the admin dashboard
                return redirect('admin_panel:dashboard')
            else:
                # Non-admin user logged in successfully but shouldn't access admin panel
                messages.error(request, 'You do not have permission to access this panel.')
                return render(request, 'login.html')
        else:
            # Authentication failed (invalid username/password or user does not exist)
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    else:
        # GET request: display the login form
        return render(request, 'login.html')

# Dashboard view using the existing template
def dashboard_view(request):
    # Basic access control: only authenticated staff/admins
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Please log in as an administrator.')
        return redirect('login')
    
    # Render the existing dashboard template
    context = {
        'username': request.user.username
    }
    return render(request, 'admin_panel/adminDashboard.html', context)
