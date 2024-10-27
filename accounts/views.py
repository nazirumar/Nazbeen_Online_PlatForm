from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from django.contrib import messages
from accounts.forms import RegisterForm
from accounts.tasks import send_activation_email, send_activation_email_task
from instructors.models import Instructor
from .utils import account_activation_token

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if Instructor.objects.filter(user=user).exists():
                messages.success(request, 'Welcome, Instructor!')
                return redirect('instructor_dashboard', request.user.public_id)
            messages.success(request, 'Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Trigger Celery task to send activation email
            send_activation_email_task.delay(user.id)
            messages.success(request, "Please check your email to activate your account.")
            return redirect('login')

        messages.error(request, "Registration failed. Please correct the errors below.")
    
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})



def activate_account(request, uidb64, token):
    try:
        # Decode the uidb64 to get the user's primary key
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the token is valid
    if user is not None and account_activation_token.check_token(user, token):
        # Activate the user account
        user.is_active = True
        user.save()
        login(request, user)  # Log the user in
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('home')  # Redirect to the home page or any other page
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')  # Redirect to the home page or a different page
