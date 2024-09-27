from django.shortcuts import get_object_or_404, render, redirect
from .models import ProfileUser, Certificate
from .forms import ProfileForms
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request, username):
    # Retrieve the user or return a 404 if not found
    user = get_object_or_404(ProfileUser, user__username=username)
    print(user)
    # Process form data on POST request
    if request.method == 'POST':
        form = ProfileForms(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.save()  # Save the form with the user instance
            return redirect('profile', username=request.user.username)  # Redirect after successful form submission
    else:
        form = ProfileForms(instance=user)  # Pre-fill the form with the user's data

    # Context to be passed to the template
    context = {
        'user': user,
        'form': form,  # Include the form in the context
    }

    return render(request, 'profile/profile.html', context)
@login_required
def certificate_view(request, user_certificate):
    certificate = get_object_or_404(Certificate, student__user__username=user_certificate)
    return render(request, 'profile/certificate.html', {'certificate': certificate})
