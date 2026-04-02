from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('download/', views.download_pdf, name='download_pdf'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  
    path('logout/', views.logout_view, name='logout'),
    path('features/', views.features_view, name='features'),
    path('privacypolicy/', views.privacypolicy_view, name='privacypolicy'),
]