from functools import wraps

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, SignupForm, UserUpdateForm


def add_bootstrap_classes(form):
    for field in form.fields.values():
        existing_classes = field.widget.attrs.get("class", "")
        field.widget.attrs["class"] = f"{existing_classes} form-control".strip()
    return form


def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper


@redirect_authenticated_user
def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect("accounts:login")
    return render(request, "accounts/signup.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Welcome back. You are now logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


@login_required
def edit_profile_view(request):
    form = UserUpdateForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated successfully.")
        return redirect("accounts:profile")
    return render(request, "accounts/edit_profile.html", {"form": form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("dashboard")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return add_bootstrap_classes(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Your password was changed successfully.")
        return response


class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.txt"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return add_bootstrap_classes(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return add_bootstrap_classes(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
