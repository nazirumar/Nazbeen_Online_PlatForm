from django.urls import path
from . import views

urlpatterns = [
    path('no-access/', views.no_access_view, name='no_access'),  # Add this line for the 'No Access' page

      # CBV =============================================================
    path('instructor/dashboard/<slug:public_id>', views.InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('instructor/my-courses/', views.MyCoursesView.as_view(), name='my_courses'),
    # path('instructor/courses/<slug:public_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    # path('instructor/courses/<slug:public_id>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    # path('instructor/courses/<slug:public_id>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    #

    path("mine/<slug:public_id>", views.ManageCourseListView.as_view(), name="instructor_course_list"),
    path("create/", views.CourseCreateView.as_view(), name="instructor_course_create"),
    path("<slug:public_id>/edit/", views.CourseUpdateView.as_view(), name="instructor_course_edit"),
    path("<slug:public_id>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
    path('<slug:public_id>/module/',views.CourseModuleUpdateView.as_view(),name='course_module_update'),
    path('module/<slug:public_id>/',views.ModuleLessonListView.as_view(),name='module_lesson_list'),
    # =============================================================
    path('module/lesson/<slug:public_id>/delete/',views.LessonDeleteView.as_view(),name='module_lesson_delete'),
    path('module/<slug:public_id>/lesson/create/', views.LessonCreateView.as_view(), name='module_lesson_create'),
    path('lesson/<slug:public_id>/edit/', views.LessonUpdateView.as_view(), name='lesson_update'),

]
