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
      # Courses
    path("courses-list/", views.ManageCourseListView.as_view(), name="instructor_course_list"),
    path("<slug:public_id>/edit/", views.CourseUpdateView.as_view(), name="instructor_course_edit"),
    path("<slug:public_id>/delete/", views.CourseDeleteView.as_view(), name="instructor_course_delete"),
    # =============================================================
    #  Modules 
    path('module-list/',views.ModuleListView.as_view(),name='instructor_module_list'),
    path('module/<slug:public_id>/edit/',views.ModuleUpdateView.as_view(),name='instructor_module_update'),
    path('module/<slug:public_id>/delete/',views.ModuleDeleteView.as_view(),name='module_delete'),
    path('module/<slug:public_id>/module/create/', views.ModuleCreateView.as_view(), name='module_create'),

    # Lessons
    path('lesson-list/',views.LessonListView.as_view(),name='instructor_lesson_list'),
    path('module/lesson/<slug:public_id>/delete/',views.LessonDeleteView.as_view(),name='instructor_lesson_delete'),
    path('lesson/<slug:public_id>/lesson/create/', views.LessonCreateView.as_view(), name='instructor_lesson_create'),
    path('lesson/<slug:public_id>/edit/', views.LessonUpdateView.as_view(), name='instructor_lesson_update'),

        # Videos
    path('video-list/',views.VideoListView.as_view(),name='instructor_video_list'),
    path('video/<slug:public_id>/delete/',views.VideoDeleteView.as_view(),name='instructor_video_delete'),
    path('video/<slug:public_id>/edit/', views.VideoUpdateView.as_view(), name='instructor_video_update'),
    
    #  Students
    path('student/<slug:public_id>/list/', views.StudentsView.as_view(), name='instructor_student_list'),
    path('student/<slug:public_id>/delete/',views.StudentsDeleteView.as_view(),name='instructor_student_delete'),
    path('certificate/list/',views.CertificatesView.as_view(),name='instructor_student_certificate'),
    path('certificates/<slug:public_id>/', views.CertificateDetailView.as_view(), name='certificate_view'),


    path('notifications/', views.notifications_view, name='notifications'),



]
