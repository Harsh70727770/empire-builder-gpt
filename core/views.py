from django.shortcuts import render, redirect
from .services.ai_engine import (
    generate_startup_plan,
    generate_idea_score,
    generate_roadmap,
    generate_tech_stack,
    generate_full_startup,
)
from django.http import FileResponse
from .utils.pdf_generator import generate_pdf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import StartupIdea, UserProfile   

# NEW HELPER FUNCTION (ONLY ADDITION)
def extract_section(text, section_name):
    if section_name not in text:
        return "⚠ Section not generated properly. Try again."

    try:
        start = text.index(section_name)
        sections = ["## Startup Plan", "## Idea Score", "## Roadmap", "## Tech Stack"]

        next_pos = len(text)

        for sec in sections:
            if sec != section_name and sec in text:
                pos = text.find(sec, start + 1)
                if pos != -1 and pos < next_pos:
                    next_pos = pos

        return text[start:next_pos].strip()

    except Exception as e:
        print("PARSE ERROR:", e)
        return "Error parsing content"


# HOME
def home(request):
    if request.method == "POST":
        idea = request.POST.get("idea")

        try:
            # SINGLE CALL (MAIN FIX)
            result = generate_full_startup(idea)
        except Exception as e:
            print("ERROR:", e)
            result = "Something went wrong. Please try again."

        # PARSE INTO SECTIONS (MAIN UPDATE)
        plan = extract_section(result, "## Startup Plan")
        score = extract_section(result, "## Idea Score")
        roadmap = extract_section(result, "## Roadmap")
        tech = extract_section(result, "## Tech Stack")

        request.session["plan"] = plan
        request.session["score"] = score
        request.session["roadmap"] = roadmap
        request.session["tech"] = tech

        return render(request, "pages/result.html", {
            "plan": plan,
            "score": score,
            "roadmap": roadmap,
            "tech": tech
        })

    return render(request, "pages/index.html")


# DOWNLOAD PDF
def download_pdf(request):
    data = {
        "plan": request.session.get("plan"),
        "score": request.session.get("score"),
        "roadmap": request.session.get("roadmap"),
        "tech": request.session.get("tech"),
    }

    if not any(data.values()):
        return redirect("dashboard")

    filename = generate_pdf(data)
    return FileResponse(open(filename, "rb"), as_attachment=True)


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

        if password != confirm_password:
            return render(request, "pages/signup.html", {"error": "Passwords do not match ❌"})

        if User.objects.filter(username=username).exists():
            return render(request, "pages/signup.html", {"error": "Username already exists ❌"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

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


# DASHBOARD
def dashboard(request):
    # FIX 1: Authentication check added
    if not request.user.is_authenticated:
        return redirect("login")

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        idea = request.POST.get("idea")

        try:
            # SINGLE CALL (MAIN FIX)
            result = generate_full_startup(idea)
        except Exception as e:
            print("ERROR:", e)
            result = "Something went wrong. Please try again."

        # PARSE INTO SECTIONS (MAIN UPDATE)
        plan = extract_section(result, "## Startup Plan")
        score = extract_section(result, "## Idea Score")
        roadmap = extract_section(result, "## Roadmap")
        tech = extract_section(result, "## Tech Stack")

        request.session["plan"] = plan
        request.session["score"] = score
        request.session["roadmap"] = roadmap
        request.session["tech"] = tech

        StartupIdea.objects.create(user=request.user, idea=idea)

        return render(request, "pages/result.html", {
            "plan": plan,
            "score": score,
            "roadmap": roadmap,
            "tech": tech
        })

    ideas = StartupIdea.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "pages/dashboard.html", {
        "ideas": ideas,
        "profile": profile
    })


# PROFILE
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'pages/profile.html', {'profile': profile})


# EDIT PROFILE
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get("phone")
        profile.country = request.POST.get("country")
        profile.state = request.POST.get("state")

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        profile.save()
        return redirect("dashboard")

    return render(request, "pages/edit_profile.html", {"profile": profile})


def about_view(request):
    return render(request, "pages/about.html")


from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        subject = f"New Contact Message from {name}"
        full_message = f"""
        Name: {name}
        Email: {email}
        Message:
        {message}
        """

        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return render(request, "pages/contact.html", {"success": True})

    return render(request, "pages/contact.html")


def features_view(request):
    return render(request, "pages/features.html")


def privacypolicy_view(request):
    return render(request, "pages/privacypolicy.html")