from django.urls import path
from courses import views

urlpatterns = [
    # Categories ========
    path("category_list/<slug:slug>", views.category_view, name="categories"),
    # Courses ========
    path("course_detail/<slug:slug>", views.category_detail_view, name="lesson_detail"),
    path("like/<int:course_id>/", views.like_course, name="like"),
    path("courses/<slug:course_id>/", views.course_detail_view, name="course_detail"
    ),  # Course details and modules
    path("course/<slug:course_id>/enroll/", views.student_enroll_course, name="student_enroll_course",),  # Enroll in a course
    # ===========
    # Lesson
    path("courses/<slug:course_id>/lessons/<slug:lesson_id>",views.lesson_detail_view, name="lesson_detail",),  # Course details and modules
    #  Module
    path("modules/<int:module_id>/courses/", views.module_courses, name="module_courses"),
    # path( "module/<slug:public_id>/", views.module_detail, name="module_detail"),  # Topics in a module
    
    path('get-content/<int:course_id>/', views.get_content, name='get_content'),



]
