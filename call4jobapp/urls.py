
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from call4jobapp import views
from .views import *
urlpatterns = [
    path('', views.login),
    path('forgot-password/', views.forgotPassword),
    path('otp-verify/<slug>/', views.otp_verify),
    path('forgot-password-form/<slug>/', views.forgotPasswordForm),
    path('logout/', views.logout),
    path('signup/', views.signup),
    path('home/', views.home, name="home"),
    path('create-job/', views.create_job, name="create_job"),
    path('job-list/', views.joblist, name="joblist"),
    path('edit-job/<slug>', views.edit_job, name="edit_job"),
    path('delete-job/<slug>', views.delete_job, name="delete_job"),
    path('view-job/<slug>', views.view_job, name="view_job"),
    path('edit-profile/<slug>', views.edit_profile, name="edit_profile"),
    path('change-password/<slug>', views.change_password),
    path('set-google-user-type/', views.save_google_type_user),
    
    
    
    
    
    
    
    
    




]
