from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy

from courses.models import Category, Course,  Module
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
import helpers
from django.contrib import messages
from .models import Category, Lesson, LessonVideo, Student, Subject, Course, Module, Enrollment
from django.contrib.auth.decorators import login_required
from courses import services 


def category_view(request, slug):
   category = get_object_or_404(Category, public_id=slug)
   subjects = category.subjects.all()

   return render(request, 'category/list.html', {'subjects':subjects})

def category_detail_view(request, slug):
   lesson = get_object_or_404(Course, public_id=slug)
   videos = lesson.lessons_video.all()
   return render(request, 'category/detail.html', {'lesson':lesson, 'videos':videos})


# Like function
@login_required
def like_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    liked_count = course.liked_by.count()

    if request.user in course.liked_by.all():
        course.liked_by.remove(request.user)
        liked_count -= 1
        return JsonResponse({'status': 'unliked', 'liked_count': liked_count})
    else:
        course.liked_by.add(request.user)
        liked_count += 1
        return JsonResponse({'status': 'liked', 'liked_count': liked_count}) 


# View to display details of a course videos title in the lesson
def course_lesson_view(request, course_id):
    course = services.get_course_detail(course_id=course_id)
    # Get all modules related to the course
    modules = course.modules.all()
    # Fetch videos and the public ID of the last lesson processed
    course_videos, last_lesson_public_id = services.get_course_lesson_videos(modules=modules)
    if request.user.is_authenticated:
        student, created = Student.objects.get_or_create(user=request.user)
        is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    else:
        is_enrolled = False
    
    context = {
        'course': course,
        'course_videos': course_videos,
        'lesson_public_id': last_lesson_public_id,
        'is_enrolled':is_enrolled
    }
    return render(request, 'courses/course_detail.html', context)

from django.http import JsonResponse
from django.shortcuts import render

def get_content(request, course_id):
    # Fetch the full course description
    course = get_object_or_404(Course, id=course_id)
    return HttpResponse(course.description)





def lesson_detail_view(request, course_id=None, lesson_id=None):
    # Retrieve the course, modules, lessons, and videos
    course_modules_lessons_video = services.get_lessons_video_watch(course_public_id=course_id)
    
    # Check if we have lessons and videos to display
    if not course_modules_lessons_video or not course_modules_lessons_video[3]:
        raise Http404("Lessons or videos not found")
    
    # Get the first video from the list for the initial playback
    initial_video = course_modules_lessons_video[3][0] if course_modules_lessons_video[3] else None
    video_embed_html = ""
    
    # Embed the first video
    if initial_video:
        video_embed_html = helpers.get_cloudinary_video_object(
            initial_video, 
            field_name='video',
            as_html=True,
            width=1250
        )
    
    # Pass data to the template
    context = {
        'video_embed_html': video_embed_html,
        'course_modules_lessons_video': course_modules_lessons_video,
    }
    return render(request, 'lesson/lessons_videos.html', context)





@login_required
def student_enroll_course(request, course_id):
    # Call the course enrollment service
    course, message = services.course_enrollment(course_id, request.user)
    
    # Add a success message to notify the user of their enrollment status
    messages.success(request, message)
    
    # Redirect to the course detail page after enrollment
    return redirect('course_detail', course_id=course.public_id)
































# View to display topics under a module
def module_detail(request, public_id):
    module = get_object_or_404(Module, public_id=public_id)
    # topics = module.le.all()
    return render(request, 'elearning/module_detail.html', {'module': module, 'topics': 'topics'})




def module_courses(request, module_id):
    module = Module.objects.get(id=module_id)
    courses = module.courses.all()  # Assuming 'courses' is the related name in the Module model
    courses_data = [{'id': course.id, 'title': course.title} for course in courses]
    return JsonResponse({'courses': courses_data})
# Enroll a student in a course