from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password_change/', views.change_password, name='password_change'),
    # path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    
    # path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    # path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),

]
