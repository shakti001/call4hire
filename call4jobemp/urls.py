
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from call4jobemp import views
from .views import *
urlpatterns = [
    path('', views.home),
    path('signup/', views.signup),
    path('signupAjax/', views.signupAjax),
    path('signupEmployementAjax/<slug>', views.signupEmployementAjax),
    path('login/', views.login, name='employee_login'),
    path('logout/', views.logout, name='employee_logout'),
    path('job-description/<slug>', views.jobDescription, name='jobDescription'),
    path('apply-job/<slug>', views.applyjob, name='applyjob'),
    path('find-job/', views.FindJobs, name='FindJobs'),
    path('about-us/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog-details/<slug>', views.blogDetails, name='blogDetails'),
    path('search/', views.search, name='search'),
    path('profile/<slug>', views.profile, name='profile'),
    path('profileSkillsSaveAjax/<slug>', views.profileSkillsSaveAjax, name='profileSkillsSaveAjax'),
    path('profileItSkillsSaveAjax/<slug>', views.profileItSkillsSaveAjax, name='profileItSkillsSaveAjax'),
    path('updateEmployementAjax/<slug>', views.updateEmployementAjax, name='updateEmployementAjax'),
    path('UpdateBasicDetailsAjax/<slug>', views.UpdateBasicDetailsAjax, name='UpdateBasicDetailsAjax'),
    path('resumeUpload/<slug>', views.resumeUpload, name='resumeUpload'),
    path('imgUpload/<slug>', views.imgUpload, name='imgUpload'),
    path('apply-jobs/<slug>', views.viewApplyJobs, name='viewApplyJobs'),
    path('about/', views.aboutMobile, name='aboutMobile'),
    



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ]