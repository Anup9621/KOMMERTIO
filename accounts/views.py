"""
Account Views
Handles user registration, login, logout, profile, and password reset
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm


def register(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('store:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_login(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('store:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Redirect to next page if exists, otherwise home
                next_page = request.GET.get('next', 'store:home')
                return redirect(next_page)
    else:
        form = UserLoginForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def user_logout_post(request):
    """
    Logout view that only accepts POST requests
    More secure as it prevents CSRF attacks
    """
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        messages.success(request, f'{username}, you have been logged out successfully.')
        return redirect('store:home')
    else:
        # If accessed via GET, redirect to home
        return redirect('store:home')


@login_required
def profile(request):
    """
    User profile view with update functionality
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'accounts/profile.html', context)


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view with email template
    """
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Password reset done confirmation
    """
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Password reset confirm view with new password form
    """
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Password reset complete confirmation
    """
    template_name = 'accounts/password_reset_complete.html'