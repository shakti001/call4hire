from django.contrib.sessions.backends.db import SessionStore
from django.utils.deprecation import MiddlewareMixin

def my_middleware(request, userData, userOtp):
    request.session['userdata'] = userData
    request.session['userOtp'] = userOtp
    

    
    # This is the middleware function
   
    return [request.session['userdata'], request.session['userOtp']]