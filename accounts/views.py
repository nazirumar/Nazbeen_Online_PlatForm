from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from accounts.forms import RegisterForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.views.generic import View
from accounts.models import CustomUser
from accounts.tasks import send_activation_email
from .utils import TokenGenerator, generate_token
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'An activation link has been sent to your email. Please check your inbox to activate your account.')
        return redirect('home')
    else:
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it's activated
            user.save()

            # Trigger the Celery task to send the activation email
            domain = request.get_host()
            send_activation_email.delay(user.pk)

            messages.success(request, "Please check your email to activate your account.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            # Decode the user ID from the base64 encoded string
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        # Check if the user exists and if the token is valid
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully. You can now log in.")
            return redirect('account:login')
        else:
            # Render an account activation failure page
            messages.error(request, "The activation link is invalid or has expired.")
            return render(request, 'accounts/activatefail.html')