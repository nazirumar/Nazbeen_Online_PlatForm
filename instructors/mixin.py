from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from courses.models import Course
from instructors.models import Instructor



class InstructorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.is_instructor(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def is_instructor(self, user):
        return Instructor.objects.filter(user=user).exists()
    
    def handle_no_permission(self):
        messages.error(self.request, 'You must be an instructor to access this page.')
        return redirect(reverse('no_access'))



class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class OwnerCourseMixin(InstructorRequiredMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'description', 'image', 'status']
    slug_field = 'public_id'
    slug_url_kwarg ='public_id'
    
    def get_success_url(self):
        # Use the slug or public_id for the success URL
        return reverse_lazy('manage_course_list', kwargs={self.slug_url_kwarg: self.object.public_id})

