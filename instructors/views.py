import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from instructors.mixin import InstructorRequiredMixin, OwnerCourseMixin, OwnerEditMixin, OwnerStudentMixin
from django.views import generic
from courses.models import Course, Lesson, LessonVideo, Module, Notification, Student
from instructors.mixin import OwnerCourseMixin
from django.views.generic.edit import FormView

from instructors.models import Certificate, Instructor

from .forms import CategoryForm, ModuleFormSet,LessonVideoFormSet, SubjectForm, CourseForm, ModuleForm, LessonForm, LessonVideoForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin




def no_access_view(request):
    """
    Renders a 'No Access' page for users without permissions.
    """
    return render(request, 'no_access.html', status=403)



# CBV ================================================


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'instructor/courses/manage/course/create_courses_form.html'





class InstructorDashboardView(InstructorRequiredMixin, generic.TemplateView):
    template_name = 'instructor/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Retrieve courses owned by the instructor
        user_courses = Course.objects.filter(owner=self.request.user)
        # Add relevant data to the context
        context['courses'] = user_courses
        context['total_courses'] = user_courses.count()
        # Count total students enrolled in the instructor's courses
        context['total_students'] = Student.objects.filter(
            enrolled_courses__in=user_courses
        ).distinct().count()
        context['students'] = Student.objects.filter(
            enrolled_courses__in=user_courses
        ).distinct()
        
        # Placeholder for average rating; you can implement this based on your requirements
        # context['average_rating'] = self.calculate_average_rating(user_courses)

        return context
    

    # def calculate_average_rating(self, courses):
    #     # Implement logic to calculate average rating across the instructor's courses
    #     # This is a placeholder; you can customize the calculation based on your rating system
    #     total_rating = sum(course.rating for course in courses if course.rating is not None)
    #     return total_rating / len(courses) if courses else 0


class MyCoursesView(InstructorRequiredMixin, generic.ListView):
    template_name = 'courses/my_courses.html'
    model = Course





class SubjectCreateView(FormView):
    template_name = 'subject_form.html'
    form_class = SubjectForm
    success_url = reverse_lazy('subject_success')  # Redirect to a success page

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class ManageCourseListView(InstructorRequiredMixin, generic.CreateView):
    model = Course
    template_name = 'instructor/courses/manage/course/list.html'
    fields = ['title', 'subject', 'description', 'access', 'status', 'image', 'price']  # Specify fields explicitly
    success_url = reverse_lazy('instructor_course_list')  # Handle redirect after successful form submission
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter courses by the owner (instructor) and order by creation date
        context["courses"] = Course.objects.filter(owner=self.request.user).order_by('-created_at')
        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).order_by('-created_at')
    
    def form_valid(self, form):
        # Save the course object and return the redirect response
        course = form.save(commit=False)
        user = self.request.user
        instructor = Instructor.objects.get(user=user)
        course.owner = user
        course.instructor = instructor
        course.save()
        return super().form_valid(form)
    



 

class ModuleCreateView(InstructorRequiredMixin, generic.View):
    form_class = ModuleFormSet
    template_name = 'instructor/modules/module_form.html'
    slug_url_kwarg = 'public_id'  # Or change it to match your model field
    
    def get(self, request, *args, **kwargs):
        # Initialize an empty formset
        print(self.kwargs.get('public_id'))

        course = get_object_or_404(Course, public_id=self.kwargs.get('public_id'))
        formset = ModuleFormSet(queryset=Module.objects.none())
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        # Process the formset
        course = get_object_or_404(Course, public_id=self.kwargs.get('public_id'))

        formset = ModuleFormSet(request.POST)
        print(formset)
        if formset.is_valid():
            modules = formset.save(commit=False)
            for module in modules:
                # Associate each module with the course
                module.course = course
                module.save()
            return redirect('instructor_lesson_create', self.kwargs.get('public_id'))
        return render(request, self.template_name, {'formset': formset})

class LessonCreateView(CreateView):
    template_name = 'instructor/lessons/lesson_form.html'
    form_class = LessonForm
    success_url = reverse_lazy('lesson_success')  # Redirect to a success page

    
    def get(self, request, *args, **kwargs):
        # Initialize both forms
        lesson_form = LessonForm()
        lesson_video_formset = LessonVideoFormSet(queryset=LessonVideo.objects.none())
        return self.render_to_response({'lesson_form': lesson_form, 'lesson_video_formset': lesson_video_formset})

    def post(self, request, *args, **kwargs):
        # Initialize the course form and module formset with POST data
        lesson_form = LessonForm(request.POST)
        lesson_video_formset = LessonVideoFormSet(request.POST)

        if lesson_form.is_valid():
           lesson = lesson_form.save(commit=False)
           module = lesson.module
           lesson.save()
           return redirect('instructor_lesson_create', module.public_id)  # Assuming your URL is using the slug/public_id

            # If the module formset is valid, save the modules
        if lesson_video_formset.is_valid():
            lesson_video = lesson_video_formset.save(commit=False)
            for lesson_video in lesson_video:
                lesson_video.save()
            return redirect('instructor_module_list')  # Assuming your URL is using the slug/public_id
        else:
            # If the forms are not valid, return the form with errors
            lesson_video_formset = LessonVideoFormSet(request.POST)

        return self.render_to_response({
            'lesson_form': lesson_form,
            'lesson_video_formset': lesson_video_formset
        })

    
    
    

class CourseUpdateView(generic.UpdateView):
    model = Course
    # permission_required = 'courses.change_course'
    template_name = 'instructor/courses/manage/course/update_form.html'
    fields = ['title','subject', 'description', 'access', 'status','image','price']
    slug_url_kwarg = 'public_id'  #
    slug_field = 'public_id'

    def get_success_url(self):
        # Ensure that public_id is either passed in context or exists in the form/model
        return reverse_lazy('instructor_course_list')

    


class CourseDeleteView(OwnerCourseMixin, generic.DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class ModuleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Module
    template_name = 'instructor/modules/update_form.html'
    form_class = ModuleForm
    slug_url_kwarg = 'public_id'
    slug_field = 'public_id'
    success_url = reverse_lazy('instructor_module_list')  # URL to redirect after success
    permission_required = 'module.change_module'




class ModuleListView(InstructorRequiredMixin, generic.CreateView):
    template_name = 'instructor/modules/list.html'
    model = Module
    fields = ['title', 'course']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modules"] = self.get_queryset().filter(course__owner=self.request.user).order_by('-created_at')
        return context
    

    def post(self, request):
        if request.method == 'POST':
            form = ModuleForm(request.POST)
            if form.is_valid():
        
                form.save()
                return redirect('instructor_module_list')
        
        return render(request, self.template_name, {'form': form})



class ModuleDeleteView(InstructorRequiredMixin, generic.DeleteView):
    model = Module
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    success_url = reverse_lazy('instructor_module_list')
    template_name = 'courses/manage/course/delete.html'




class LessonListView(InstructorRequiredMixin, generic.CreateView):
    template_name = 'instructor/lessons/list.html'
    model = Lesson
    fields = ['title', 'description', 'module', 'thumbnail']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = self.get_queryset().filter(module__course__owner=self.request.user).order_by('-created_at')
        return context
    

    def post(self, request):
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
        
                form.save()
                return redirect('instructor_lesson_list')
        
        return render(request, self.template_name, {'form': form})


class LessonDeleteView(InstructorRequiredMixin, generic.DeleteView):
    model = Lesson
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    success_url = reverse_lazy('instructor_lesson_list')
    template_name = 'courses/manage/course/delete.html'



# Lesson Update View
class LessonUpdateView(InstructorRequiredMixin, generic.UpdateView):
    model = Lesson
    fields = ['title', 'description', 'module', 'thumbnail']
    permission_required = 'lessons.change_lesson'
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    success_url = reverse_lazy('instructor_lesson_list')
    template_name = 'instructor/lessons/update_form.html'



class VideoListView(InstructorRequiredMixin, generic.CreateView):
    template_name = 'instructor/lessonvideos/list.html'
    model = LessonVideo
    fields = ['title', 'lesson', 'video']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vidoes"] = self.get_queryset().filter(lesson__module__course__owner=self.request.user).order_by('-created_at')
        return context
    

    def post(self, request):
        if request.method == 'POST':
            form = LessonVideoForm(request.POST)
            if form.is_valid():
                print(form)
                form.save()
                return redirect('instructor_video_list')
        
        return render(request, self.template_name, {'form': form})


class VideoUpdateView(InstructorRequiredMixin, generic.UpdateView):
    model = LessonVideo
    fields = ['title', 'lesson', 'video']
    permission_required = 'lessons.change_lesson'
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    success_url = reverse_lazy('instructor_video_list')
    template_name = 'instructor/lessonvideos/update_form.html'

class VideoDeleteView(InstructorRequiredMixin, generic.DeleteView):
    model = LessonVideo
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    success_url = reverse_lazy('instructor_video_list')
    template_name = 'courses/manage/course/delete.html'



class StudentsView(InstructorRequiredMixin, generic.ListView):
    template_name = 'instructor/students/list.html'
    model = Student

    def get_queryset(self):
        user_courses = Course.objects.filter(owner=self.request.user)
        return super().get_queryset().filter(enrolled_courses__in=user_courses).distinct()

class StudentsDeleteView(InstructorRequiredMixin, generic.DeleteView):
    model = Student
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    template_name = 'courses/manage/course/delete.html'


    def get_success_url(self):
        # Ensure that public_id is either passed in context or exists in the form/model
        return reverse_lazy('instructor_student_list', kwargs={self.slug_url_kwarg: self.object.public_id} )

class CertificatesView(InstructorRequiredMixin, generic.ListView):
    template_name = 'instructor/certificates/list.html'
    model = Certificate


class CertificateDetailView(InstructorRequiredMixin, generic.DetailView):
    model = Certificate
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'
    template_name =  "instructor/certificates/certificate_view.html"

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_POST
def notifications_view(request):
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        notification_id = data.get('notification_id')  # Get notification_id from JSON data

        if notification_id:
            # Fetch the notification and mark it as viewed
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid notification ID'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)