from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_View(request):
    print('begin 1')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'login.html')
        print(username)
        print(password)

        # Attempt to authenticate using username
        user = authenticate(username=username, password=password)
        print('begin 3')
        print(username)
        print(password)

        if user is not None:
            login(request, user)
            print('begin 4')
            print(username)
            print(password)

            return redirect('admin_panel:dashboard')

        else:
            print('begin 5')
            print(username)

            return render(request, 'login.html')

    else:
        print('begin 6')

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
