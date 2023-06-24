
from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path("register/", RegisterUser.as_view()),
    path("login/", LoginUser.as_view()),
    path("verify-email-otp/", VerifyEmailOTP.as_view()),
    
    
]
    
    
    
    
    
    
    
    
    
    