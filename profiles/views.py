from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from courses.models import Course, Enrollment, Notification, Student
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
    


class StudentNotificationView(LoginRequiredMixin, generic.DetailView):
    template_name = 'students/notification.html'
    model = Notification
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    def get_queryset(self):
        return super().get_queryset().filter(student=self.request.user)
    
    def get(self, request, *args, **kwargs):
        """
        Override the get method to mark the notification as read
        when it's accessed by the student.
        """
        # Mark the notification as read
        notification = self.get_object()  # Get the specific notification object
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return super().get(request, *args, **kwargs)

    

class StudentCoursesView(LoginRequiredMixin, generic.ListView):
    template_name = 'students/student_courses.html'
    model = Course
    context_object_name = 'enrolled_courses'


    
    def get_queryset(self):
        # Get the list of courses that the student is enrolled in
        student = Student.objects.get(user=self.request.user)
        enrolled_courses = Course.objects.filter(enrollments__student=student)
        return enrolled_courses