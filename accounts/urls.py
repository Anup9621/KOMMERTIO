"""
Accounts URL Configuration
Maps URLs to authentication views
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration and login
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
    
    # Password reset
    path('password-reset/', 
         views.CustomPasswordResetView.as_view(), 
         name='password_reset'),
    path('password-reset/done/', 
         views.CustomPasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         views.CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         views.CustomPasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
]