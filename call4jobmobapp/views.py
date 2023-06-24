from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import *
from call4jobapp.models import *
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from django.contrib.auth.models import auth
import json
from call4jobapp.helpers import *
from .session_middleware import *
 # Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        try:
            data= request.data
            if data:
                serializer = RegitserSerializer(data=data)
                if serializer:
                    if not User.objects.filter(email=data["email"].lower()).exists():
                        if not User.objects.filter(phone_number=data["phone_number"]).exists():
                            if serializer.is_valid(raise_exception=False):
                                if data["login_source"] == 0:
                                    if not data["email"]:
                                        return JsonResponse({"status": False, "message": "Folowing field are required: email" })
                                    elif not data["username"]:
                                        return JsonResponse({"status": False, "message": "Folowing field are required: name",})
                                    elif not data['country_code']:
                                        
                                        return JsonResponse({"status": False, "message": "Folowing field are required: country code",})
                                    elif not data['phone_number']:
                                        
                                        return JsonResponse({"status": False, "message": "Folowing field are required: phone number",})
                                    elif not data['office_address']:
                                        
                                        return JsonResponse({"status": False, "message": "Folowing field are required: office address",})
                                    elif not data['home_address']:
                                        return JsonResponse({"status": False, "message": "Folowing field are required: Home address",})
                                    elif not data['dob']:
                                        
                                        return JsonResponse({"status": False, "message": "Folowing field are required: date of birth",})
                                    elif not data['password']:
                                        
                                        return JsonResponse({"status": False, "message": "Folowing field are required: password",})
                                    elif not data['gender']:
                                        return JsonResponse({"status": False, "message": "Folowing field are required: gender",})
                                    else:
                                        otp = generateOTP()
                                        subject = "One Time Password Has been sent."
                                        message = f"Your One time Password is {otp}"
                                        recipient = [data['email']]
                                        sent_mail = sendMail(subject, message, recipient)
                                        request.session['userdata'] = data
                                        request.session['userOtp'] = otp
                                        return JsonResponse({"status": True, "message": "Verification code sent on the mail address. Please check !!!!"})
                            else:
                                return JsonResponse({"status": False, "message": "data is not valid it's not in json format !"})  
                        else:
                            return JsonResponse({"status": False, "message": "Phone number allready exits !!!"})   
                else:
                    return JsonResponse({"status": False, "message": "Data format not support !!!"})    
            else:
                return JsonResponse({"status": False, "message": "Something went wrong!"})        
        except MultiValueDictKeyError as e:
                missing_key_name =e.args[0]                
                return JsonResponse({"status":"False", "Your Missing key": f"{missing_key_name}"})        
                


class VerifyEmailOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            if data:
                serializer = VerifyOTPSerializer(data=data)
                if serializer.is_valid():
                    if data['email'] == request.session['userdata']['email']:
                        print(request.session['userOtp'])
                        if request.session['userOtp'] == data["otp"]:
                            try:
                                if  User.objects.get(email = request.session['userdata']['email'].lower()):
                                    return Response(
                                    {
                                        "status": False,
                                        "message": "User allready exits please try again later.",
                                    }
                                ) 
                            except:
                                user = User.objects.create(email=request.session['userdata']['email'].lower(), roll="employee",
                                username = request.session['userdata']['username'],
                                country_code = request.session['userdata']['country_code'],
                                phone_number = request.session['userdata']['phone_number'],
                                office_address = request.session['userdata']['office_address'],
                                home_address = request.session['userdata']['home_address'],
                                dob = request.session['userdata']['dob'],
                                is_active = True,
                                # fcm_token =request.session['userdata']['fcm_token'],
                                password = make_password(request.session['userdata']['password']),
                                email_verified = 1
                                )
                                token = Token.objects.get_or_create(user_id=user.id)
                                return Response(
                                    {
                                        "status": True,
                                        "token": str(token),
                                        "message": "Email Verification is successfully completed Please login !!!!!",
                                    }
                                )
                        else:
                            return Response(
                                {
                                    "status": False,
                                    "message": "OTP not match. Please try again.",
                                }
                            )
                   
                    else:
                        return Response(
                            {
                                "status": False,
                                "message": "Email id is not match with register email Please register again!",
                            }
                        )
            else:
                return Response(
                    {
                        "status": False,
                        "message": "Please Input validate data!",
                    }
                )
        except:
            return Response(
                {
                    "status": False,
                    "message": "Something went wrong!",
                }
            )




class LoginUser(APIView):
    def post(self, request):
            data = request.data
            if data:
                serializer = LoginSerializer(data=data)
                if serializer.is_valid():
                    if User.objects.filter(email=data["email"].lower()).exists():                        
                        user = User.objects.get(email=data["email"].lower())
                        if user.check_password(data["password"]):
                            if user.email_verified == False:
                                return Response(
                                    {
                                        "status": True,
                                        "is_verified": user.is_verified,
                                        "message": "Your Email address is not verified yet.",
                                    }
                                )
                            if not user.is_active == True:
                                return Response(
                                    {
                                        "status": False,
                                        "message": "Your Account is Inactive. Please contact the Admin.",
                                    }
                                )
                            if not user.check_password(data["password"]):
                                return Response(
                                    {
                                        "status": False,
                                        "message": "Incorrect Password. Please try again!",
                                    }
                                )
                            else:
                                try:
                                    user = User.objects.get(email = data["email"].lower() )                              
                                    if user:
                                        if data["login_source"] == 0:
                                            user.fcm_token = data['fcm_token']
                                            user.login_source = 0
                                            user.save()
                                            auth.authenticate(
                                            email=data["email"].lower(), password=data["password"]
                                            )
                                            auth.login(request, user)
                                            token = Token.objects.get_or_create(user_id=user.id)
                                            return Response(
                                                {
                                                    "status": True,
                                                    "token": str(token),
                                                    "message": "Login Success.",
                                                }
                                            )
                                except:
                                    return Response(
                                        {
                                            "status": False,
                                            "message": "Email not found",
                                        }
                                    )
                                    
                        else:
                            return Response(
                                {
                                    "status": False,
                                    "message": "Incorrect Password. Please try again!",
                                }
                            )
                    else:
                        return Response(
                            {
                                "status": False,
                                "message": "Email not found.",
                            }
                        )
                else:
                    return Response(
                        {
                            "status": False,
                            "message": "Please Input validate data...",
                        }
                    )
            else:
                return Response(
                    {
                        "status": False,
                        "message": "Please Input validate data...",
                    }
                )
      
