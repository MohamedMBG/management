from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages

from client_panel.models import Client


# def signup_View(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         role = request.POST.get('role')
#         if form.is_valid() and role in ['freelancer', 'client']:
#             user = form.save(commit=False)
#             user.save()
#             group = Group.objects.get(name=role)
#             user.groups.add(group)
#
#             login(request, user)
#             messages.success(request, f"Account created successfully as a {role}.")
#             return redirect('login')
#         else:
#             messages.error(request, "Please complete the form correctly.")
#     else:
#         form = UserCreationForm()
#     return render(request, 'client_panel/signup.html',{'form':form})

def signup_View(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')

        if form.is_valid() and role == 'client':
            user = form.save(commit=False) #like if we make the client column but just with the id
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # On ajoute l'utilisateur au groupe "client"
            user.groups.add(Group.objects.get(name='client'))

            # On crée le profil client lié à cet utilisateur
            Client.objects.create(
                user=user,
                email=user.email,
                telephone=request.POST.get('telephone'),
                adresse=request.POST.get('adresse')
            )

            login(request, user)
            messages.success(request, "Client account created successfully.")
            return redirect('client_signin')  # Or wherever you want
        else:
            messages.error(request, "Please complete the form correctly.")
    else:
        form = UserCreationForm()

    return render(request, 'client_panel/signup.html', {'form': form})

def signin_View(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('some_dashboard') # update as needed
    return render(request, 'client_panel/signin.html', {'form': form})

def signout_View(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté(e) avec succès.")
    return redirect('client_signin')

def dashboard_View(request):
    return render(request, 'client_panel/dashboard.html')