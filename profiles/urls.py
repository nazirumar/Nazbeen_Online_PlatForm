from django.urls import path
from . import views

urlpatterns = [
    path('profile/<username>', views.profile_view, name='profile'),
    path('certificate/<slug:public_id>', views.StudentCertificatesView.as_view(), name='user_certificate'),
    path('student-notification/<slug:public_id>', views.StudentNotificationView.as_view(), name='student_notification'),
    path('courses/<slug:public_id>', views.StudentCoursesView.as_view(), name='student_courses'),


]
