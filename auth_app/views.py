from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import RegistrationForm

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("auth_app:dashboard")
    else:
        form = RegistrationForm()
    return render(request, "auth_app/register.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "auth_app/dashboard.html")

@login_required
def profile(request):
    return render(request, "auth_app/profile.html")

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect("auth_app:profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "auth_app/change_password.html", {"form": form})
