from django.shortcuts import render, redirect
from .services.ai_engine import (
    generate_startup_plan,
    generate_idea_score,
    generate_roadmap,
    generate_tech_stack
)
from django.http import FileResponse
from .utils.pdf_generator import generate_pdf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import StartupIdea, UserProfile   

import markdown

# HOME
def home(request):
    if request.method == "POST":
        idea = request.POST.get("idea")

        # RAW OUTPUT
        plan_raw = generate_startup_plan(idea)
        score_raw = generate_idea_score(idea)
        roadmap_raw = generate_roadmap(idea)
        tech_raw = generate_tech_stack(idea)

        # CONVERT TO HTML
        plan = markdown.markdown(plan_raw, extensions=['extra'])
        score = markdown.markdown(score_raw, extensions=['extra'])
        roadmap = markdown.markdown(roadmap_raw, extensions=['extra'])
        tech = markdown.markdown(tech_raw, extensions=['extra'])

        # SAVE TO SESSION (RAW for PDF)
        request.session["plan"] = plan_raw
        request.session["score"] = score_raw
        request.session["roadmap"] = roadmap_raw
        request.session["tech"] = tech_raw

        return render(request, "pages/result.html", {
            "plan": plan,
            "score": score,
            "roadmap": roadmap,
            "tech": tech
        })

    return render(request, "pages/index.html")


# DOWNLOAD PDF (UNCHANGED)
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
import markdown
import re

def extract_scores(text):
    market = re.search(r'Market.*?(\d+)/10', text)
    competition = re.search(r'Competition.*?(\d+)/10', text)
    profit = re.search(r'Profit.*?(\d+)/10', text)
    overall = re.search(r'(\d+)/100', text)

    return {
        "market": market.group(1) if market else "0",
        "competition": competition.group(1) if competition else "0",
        "profit": profit.group(1) if profit else "0",
        "overall": overall.group(1) if overall else "0",
    }


def download_pdf(request):
    data = {
        "plan": request.session.get("plan"),
        "score": request.session.get("score"),
        "roadmap": request.session.get("roadmap"),
        "tech": request.session.get("tech"),
    }

    if not any(data.values()):
        return redirect("dashboard")

    # ✅ Extract dynamic scores
    scores = extract_scores(data["score"])

    context = {
        "plan": markdown.markdown(data["plan"], extensions=['extra']),
        "score": markdown.markdown(data["score"], extensions=['extra']),
        "roadmap": markdown.markdown(data["roadmap"], extensions=['extra']),
        "tech": markdown.markdown(data["tech"], extensions=['extra']),

        # ✅ Dynamic values
        "market_score": scores["market"],
        "competition_score": scores["competition"],
        "profit_score": scores["profit"],
        "overall_score": scores["overall"],
    }

    html = render_to_string("pages/pdf_template.html", context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="startup_report.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response


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


# SIGNUP (UNCHANGED)
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
    if not request.user.is_authenticated:
        return redirect("login")

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        idea = request.POST.get("idea")

        # RAW
        plan_raw = generate_startup_plan(idea)
        score_raw = generate_idea_score(idea)
        roadmap_raw = generate_roadmap(idea)
        tech_raw = generate_tech_stack(idea)

        # HTML
        plan = markdown.markdown(plan_raw, extensions=['extra'])
        score = markdown.markdown(score_raw, extensions=['extra'])
        roadmap = markdown.markdown(roadmap_raw, extensions=['extra'])
        tech = markdown.markdown(tech_raw, extensions=['extra'])

        request.session["plan"] = plan_raw
        request.session["score"] = score_raw
        request.session["roadmap"] = roadmap_raw
        request.session["tech"] = tech_raw

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

        #  Save to Database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        #  Send Email
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
    return render(request,"pages/privacypolicy.html")