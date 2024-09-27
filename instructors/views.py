from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from instructors.forms import LessonForm
from instructors.mixin import InstructorRequiredMixin, OwnerCourseMixin, OwnerEditMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from courses.models import Course, Lesson, Module
from instructors.mixin import OwnerCourseMixin


def no_access_view(request):
    """
    Renders a 'No Access' page for users without permissions.
    """
    return render(request, 'no_access.html', status=403)



# CBV ================================================


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'instructor/courses/manage/course/list.html'
    permission_required = 'courses.view_course'
    
    def get_queryset(self):
        # Filter courses by the logged-in user's username
        username = self.request.user.username
        return Course.objects.filter(owner__username=username)



class InstructorDashboardView(InstructorRequiredMixin, TemplateView):
    template_name = 'instructor/index.html'
    


class MyCoursesView(InstructorRequiredMixin, ListView):
    template_name = 'courses/my_courses.html'
    model = Course


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    fields = ['description', 'image','access','status','price','subject' ]
    success_url = reverse_lazy('manage_course_list')

    def form_valid(self, form):
        # Here you can modify the form instance before saving, if necessary
        # For example, you can set the owner to the current user
        form.instance.owner = self.request.user  # Assuming you have an `owner` field
        print(form.cleaned_data)  # It's better to use cleaned_data for debug
        return super().form_valid(form)
    


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

    


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(UpdateView):
    model = Course
    fields = ['title', 'description']  # Fields for the Course form
    template_name = 'courses/manage/module/formset.html'
    success_url = reverse_lazy('manage_course_list')  # Redirect URL after saving
    slug_field = 'public_id'
    slug_url_kwarg ='public_id'

    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # Create a formset for the related Module model
            ModuleFormSet = modelformset_factory(Module, fields=['title'], extra=1, can_delete=True)
            context['modules'] = ModuleFormSet(queryset=self.object.modules.all())
            return context



    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Retrieve the management form from the POST data
        total_forms = int(self.request.POST.get('modules-TOTAL_FORMS', 0))  # default to 0 if not found

        for i in range(total_forms):
            # Check if the delete checkbox is checked
            if self.request.POST.get(f'modules-{i}-DELETE'):
                module_id = self.request.POST.get(f'modules-{i}-id')  # Ensure you have the correct ID
                if module_id:  # Only delete if there's a valid ID
                    Module.objects.filter(id=module_id).delete()
            else:
                # Here you would handle updating or creating new modules
                # Ensure you handle the creation/update logic
                pass

        return response


        
    
# class LessonCreateUpdate(TemplateResponseMixin, View):
#     module = None
#     model = None
#     obj = None
#     template_name = 'courses/manage/module/form.html'
#     slug_field ='public_id'
#     slug_url_kwarg ='ublic_id'

#     def get_model(self, model_name):
#         if model_name in 


class ModuleLessonListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'
    slug_field ='public_id'
    slug_url_kwarg ='public_id'

    def get(self, request, public_id):
        module = get_object_or_404(Module, public_id=public_id, course__owner=request.user)
        return render(request, self.template_name, {'module': module})

class LessonDeleteView(View):
    def post(self, request, public_id):
        lesson = get_object_or_404(Lesson, public_id=public_id, module__course__owner=request.user)
        module = lesson.module
        lesson.delete()
        return redirect('module_lesson_list', module.public_id)



# Mixin for shared logic
class LessonMixin:
    model = Lesson
    form_class = LessonForm
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    template_name = 'courses/manage/lesson/form.html'  # Path to your form template

    def get_success_url(self):
        # Redirect to a detailed view or list of lessons after success
        return reverse_lazy('module_lesson_list', kwargs={'public_id': self.object.module.public_id})

# Lesson Create View
class LessonCreateView(LessonMixin, CreateView):
    permission_required = 'lessons.add_lesson'
 

    def form_valid(self, form):
        return super().form_valid(form)


# Lesson Update View
class LessonUpdateView(LessonMixin, UpdateView):
    permission_required = 'lessons.change_lesson'

    def get_object(self, queryset=None):
        # Ensure we retrieve the object using the public_id instead of the pk
        return get_object_or_404(Lesson, public_id=self.kwargs.get('public_id'))



