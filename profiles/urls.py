from django.urls import path
from . import views

urlpatterns = [
    path('profile/<username>', views.profile_view, name='profile'),
    path('certificate/<user_certificate>', views.certificate_view, name='user_certificate'),
    
]
