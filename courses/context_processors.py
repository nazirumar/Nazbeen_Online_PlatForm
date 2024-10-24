from django.shortcuts import get_object_or_404
from courses.models import Category, Course, Notification
from instructors.models import Instructor

# context_processors.py
def category(request):
    categories = Category.objects.all()
    return {'categories': categories}



def instructor_tag(request):
     # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Attempt to retrieve the instructor related to the logged-in user
            instructor = Instructor.objects.get(user=request.user)
             # Fetch all courses related to the instructor
            instructor_courses = Course.objects.filter(instructor=instructor)
            print(instructor_courses)
            # Filter notifications related to the instructor's courses and not yet read
            notifications = Notification.objects.filter(course__in=instructor_courses, is_read=False)
            print(notifications)
            if request.method == 'POST':
                # Mark all notifications as read if a POST request is made
                notifications.update(is_read=True)
        except Instructor.DoesNotExist:
            instructor = None
            notifications = None
    else:
        # If the user is not authenticated, set instructor to None
        instructor = None
        notifications = None

    return {'instructor': instructor, 'notifications': notifications}
