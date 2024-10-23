from email.message import EmailMessage
from django.core.mail import EmailMessage
from .forms import RegistrationForm
from .models import Account
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.http import HttpResponse
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = email.split("@")[0]
            password = form.cleaned_data['password']
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            ) 
            user.phone_number = phone_number
            user.save()
            # user activation 
            current_site = get_current_site(request)
            email_subject = "Activate Your Account"
            message = render_to_string('accounts/activate_email.htm', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'You are successfully registered, Please check your email for account activation link')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, "accounts/register.htm", context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are successfully loged-in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, "accounts/login.htm")

@login_required(login_url = 'login') # To ensure only the loged in accounts can perform the logout
def logout_view(request):
    auth.logout(request)  # Logs out the user
    messages.success(request, "You have been logged out successfully.") 
    return redirect('login')

def activate_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations your account is activated ')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link or token expired')
        return redirect('register')
    
@login_required(login_url = 'login') # To ensure only the loged in accounts goes to dashboard 
def dashboard(request):
    return render(request, "accounts/dashboard.htm")