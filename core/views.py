from django.shortcuts import render
from .services.ai_engine import (
    generate_startup_plan,
    generate_idea_score,
    generate_roadmap,
    generate_tech_stack
)
from .utils.formatters import parse_response

def home(request):
    if request.method == "POST":
        idea = request.POST.get("idea")

        plan = generate_startup_plan(idea)
        score = generate_idea_score(idea)
        roadmap = generate_roadmap(idea)
        tech = generate_tech_stack(idea)

        return render(request, "pages/result.html", {
            "plan": plan,
            "score": score,
            "roadmap": roadmap,
            "tech": tech
        })

    return render(request, "pages/index.html")

from django.http import FileResponse
from .utils.pdf_generator import generate_pdf

def download_pdf(request):
    data = request.session.get("data")

    filename = generate_pdf(data)
    return FileResponse(open(filename, "rb"), as_attachment=True)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import StartupIdea, UserProfile   

# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "pages/login.html")

# SIGNUP
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        phone = request.POST.get("phone")
        country = request.POST.get("country")
        state = request.POST.get("state")

        # Password match check
        if password != confirm_password:
            return render(request, "pages/signup.html", {
                "error": "Passwords do not match ❌"
            })

        # Username exists check
        if User.objects.filter(username=username).exists():
            return render(request, "pages/signup.html", {
                "error": "Username already exists ❌"
            })

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # CREATE USER PROFILE (NEW)
        UserProfile.objects.create(
            user=user,
            phone=phone,
            country=country,
            state=state
        )

        return redirect("login")

    return render(request, "pages/signup.html")

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    ideas = StartupIdea.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "pages/dashboard.html", {"ideas": ideas})