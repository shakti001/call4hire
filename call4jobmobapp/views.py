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
# Create your views here.
class RegisterUser(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data["dob"])
            
            print(data["fcm_token"])
            if data:
                serializer = RegitserSerializer(data=data,many=True)
                if serializer:
                    if not User.objects.filter(email=data["email"].lower()).exists():
                        if not User.objects.filter(phone_number=data["phone_number"]).exists():
                            if serializer.is_valid(raise_exception=False):
                                if data["login_source"] == '0':
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
                                    elif not data['fcm_token']:
                                        return JsonResponse({"status": False, "message": "Folowing field are required: Fcm token are missing",})
                                    
                                    else:
                                        user = User.objects.create(email=data["email"].lower(), roll="employee",
                                        username = data["username"],
                                        country_code = data["country_code"],
                                        phone_number = data["phone_number"],
                                        office_address = data["office_address"],
                                        home_address = data["home_address"],
                                        dob = data["dob"],
                                        is_active = True,
                                        fcm_token = data['fcm_token'],
                                        password = make_password(data["password"])
                                        )
                                        if user:
                                            token, created = Token.objects.get_or_create(user_id=user.id)
                                            return JsonResponse({"status": True, "message": "Register Succesfully !!!!"})
                                        else:
                                            return JsonResponse({"status": False, "message": "Something is missing !!!!"})
                            else:
                                return JsonResponse({"status": False, "message": "All fields required!"})  
                        else:
                            return JsonResponse({"status": False, "message": "Phone number allready exits !!!"})   
                    else:
                        return JsonResponse({"status": False, "message": "Email allready exits !!!"})    
                else:
                    return JsonResponse({"status": False, "message": "Data format not support !!!"})    
            else:
                return JsonResponse({"status": False, "message": "Something went wrong!"})        
        
        except MultiValueDictKeyError:
            return JsonResponse({"status": False, "message": "Any data Key is missing "})

class LoginUser(APIView):
    def post(self, request):
        # try:
            data = request.data
            if data:
                serializer = LoginSerializer(data=data)
                if serializer.is_valid():
                    if User.objects.filter(email=data["email"].lower()).exists():
                        user = User.objects.get(email=data["email"].lower())
                        if user:
                            # user = 
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
                            #     user_view = UserViewSerializer(user)
                            #     refresh = RefreshToken.for_user(user)
                              
                            #     auth.authenticate(
                            #         email=data["email"].lower(), password=data["password"]
                            #     )
                            #     auth.login(request, user)
                                return Response(
                                    {
                                        "status": True,
                                        # "token": str(refresh.access_token),
                                        # "payload": user_view.data,
                                        "message": "Login Success.",
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
        # except:
        #     return Response(
        #         {
        #             "status": False,
        #             "message": "Something went wrong!",
        #         }
        #     ) 