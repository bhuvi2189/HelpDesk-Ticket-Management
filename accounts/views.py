
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# User Registration

# User Registration
def register(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not email or not password:
            error = "All fields are required."

        elif User.objects.filter(username__iexact=username).exists():
            error = "Username already exists."

        elif User.objects.filter(email__iexact=email).exists():
            error = "Email already registered."

        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect("login")

    return render(
        request,
        "accounts/register.html",
        {"error": error}
    )


# User Login
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")

            return redirect("employee_dashboard")

        else:

            return render(
                request,
                "accounts/login.html",
                {
                    "error": "Invalid username or password"
                }
            )

    return render(
        request,
        "accounts/login.html"
    )


# User Dashboard
@login_required
def dashboard(request):

    return render(
        request,
        "accounts/dashboard.html"
    )


# User Profile
@login_required
def profile(request):

    error = ""

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name", ""
        ).strip()

        last_name = request.POST.get(
            "last_name", ""
        ).strip()

        email = request.POST.get(
            "email", ""
        ).strip()

        if not first_name or not email:

            error = "First name and email are required."

        elif User.objects.filter(
            email__iexact=email
        ).exclude(id=request.user.id).exists():

            error = "This email is already being used."

        else:

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()

            return redirect("profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "error": error,
            "user": request.user
        }
    )


# User Logout
def user_logout(request):

    logout(request)

    return redirect("login")
