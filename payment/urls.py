from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/payment-success/', views.payment_success, name='payment_success'),
]