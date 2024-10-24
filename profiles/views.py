from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from instructors.models import Certificate
from io import BytesIO
from django.core.files import File
from instructors.models import Certificate
from profiles.models import ProfileUser
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
def certificate_view(request, public_id):
    certificate = get_object_or_404(Certificate, student__user__public_id=public_id)
    return render(request, 'profile/certificate.html', {'certificate': certificate})



class StudentCertificatesView(LoginRequiredMixin, generic.ListView):
    template_name = 'profile/certificate.html'
    model = Certificate
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    def get_queryset(self):
        return super().get_queryset().filter(student__user=self.request.user)