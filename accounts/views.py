from django.shortcuts import render
from .forms import RegistrationForm
# Create your views here.

def register(request):
    form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.htm', context)

def login(request):
    return render(request, 'accounts/login.htm')

def logout(request):
    return render(request, 'accounts/logout.htm')