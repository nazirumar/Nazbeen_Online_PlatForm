from django.shortcuts import get_object_or_404
from courses.models import Category, Course, Notification
from instructors.models import Instructor
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


# context_processors.py
def category(request):
    categories = Category.objects.all()
    return {'categories': categories}



def instructor_tag(request):
      # Initialize default values
    instructor = None
    notifications = None
    if request.user.is_authenticated:
        try:
            # Retrieve the instructor related to the logged-in user
            instructor = Instructor.objects.get(user=request.user)
            
            # Fetch all courses related to the instructor
            instructor_courses = Course.objects.filter(instructor=instructor)
            # Filter notifications related to the instructor's courses and unread ones
            notifications = Notification.objects.filter(course__in=instructor_courses, is_read=False).order_by('-timestamp')

        except Instructor.DoesNotExist:
            # Log or handle the case where the instructor is not found
            pass

        except ObjectDoesNotExist:
            # Handle the case when no notifications or courses exist
            pass
    else:
        # Log or handle the case where the user is not authenticated
        pass

    return {'instructor': instructor, 'notifications': notifications}