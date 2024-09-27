from django.shortcuts import get_object_or_404, render

from courses import services 



def home(request):
    courses = services.get_publish_courses().order_by('-created_at')
    courses_likes = []
    for course in courses:
        liked_count = course.liked_by.count() 
        courses_likes.append((course,liked_count))
    return render(request, 'index.html', {'courses_likes': courses_likes, 'courses':courses})

def about(request):
    return render(request, 'pages/about.html')