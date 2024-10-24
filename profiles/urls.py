from django.urls import path
from . import views

urlpatterns = [
    path('profile/<username>', views.profile_view, name='profile'),
    path('certificate/<slug:public_id>', views.StudentCertificatesView.as_view(), name='user_certificate'),

]
