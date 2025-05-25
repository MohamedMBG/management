from django.shortcuts import render

def login_View(request):
    return render(request , 'login.html')