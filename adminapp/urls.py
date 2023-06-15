
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from adminapp import views
from .views import *
urlpatterns = [
    path('', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('userlist/', views.userlist),
    path('add-userlist/', views.add_userlist),
    path('edit-userlist/<slug>', views.edit_userlist),
    path('delete-userlist/<slug>', views.delete_userlist),
    path('view-userlist/<slug>', views.view_userlist),
    path('employeeList/', views.empList),
    path('view-emplist/<slug>', views.view_empList),
    path('delete-emplist/<slug>', views.delete_emplist),



    
    path('add-subadmin/', views.add_subadmin),
    path('subadmin/', views.subadmin),
    path('edit-subadmin/<slug>', views.edit_subadmin),
    path('delete-subadmin/<slug>', views.delete_subadmin),
    path('view-subadmin/<slug>', views.view_subadmin),
    path('userStatusAjax/<int:user_id>', views.userStatusAjax , name="userStatusAjax"),
    path('edit-profile/<slug>', views.edit_profile),
    path('change-password/<slug>', views.change_password),
    path('forgot-password/', views.forgotPassword),
    path('otp-verify/<slug>/', views.otp_verify),
    path('forgot-password-form/<slug>/', views.forgotPasswordForm),
    path('job-list/', views.joblist),
    path('add-joblist/', views.add_joblist),
    path('edit-joblist/<slug>', views.edit_joblist),
    path('delete-joblist/<slug>', views.delete_joblist),
    path('view-joblist/<slug>', views.view_joblist),
    path('job-status-ajax/<int:id>', views.job_status_ajax),
    path('assign-job-ajax/<int:id>', views.assign_job__ajax),
    path('company_user_ajax/', views.company_user_ajax),
    path('assign-job-list/<slug>', views.assignJoblist),
    path('job-category/', views.jobCategory),
    path('add-category/', views.add_category),
    path('edit-category/<slug>', views.edit_category),
    path('delete-category/<slug>', views.delete_category),
    path('change-job-status/<int:id>', views.assign_job_status, name="change_job_status"),
    path('cms-pages/', views.cmspageList, name="cmspageList"),
    
    
    path('edit-cms-pages/<slug>', views.csmPage, name="csmPage"),
    path('blog/', views.blog, name="blog"),
    path('add-blog/', views.add_blog, name="add_blog"),
    path('edit-blog/<slug>/', views.edit_blog, name="edit_blog"),
    path('delete-blog/<slug>/', views.delete_blog, name="delete_blog"),
    path('blogCategory/', views.blogCategory, name="blogCategory"),
    path('add-blogCategory/', views.add_blogCategory, name="add_blogCategory"),
    path('edit-blogCategory/<slug>/', views.edit_blogCategory, name="edit_blogCategory"),
    path('delete-blogCategory/<slug>/', views.delete_blogCategory, name="delete_blogCategory"),
    path('view-assign-Job/', views.ViewassignJob, name="ViewassignJob"),
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    





]
