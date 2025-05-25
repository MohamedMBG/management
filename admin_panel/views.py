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
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            userGroup = request.user.groups.first()
            if userGroup :
                if userGroup == 'administrateur':
                    return redirect('admin_panel:dashboard')
                if userGroup == 'superviseur':
                    return redirect()
                if userGroup == 'client':
                    return redirect()
            else:
                return render(request, 'login.html')

        else:
            return render(request, 'login.html')

    else:
        return render(request,'login.html')

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
