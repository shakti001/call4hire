from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import *
from call4jobapp.models import *
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
class RegisterUser(APIView):
    def post(self, request):
        try:
            data = request.data
            if data:
           
                serializer = RegitserSerializer(data=data,many=True)
                if serializer:
                    if not User.objects.filter(email=data["email"].lower()).exists():
                        if serializer.is_valid(raise_exception=False):
                            user = User(email=data["email"].lower(), roll=data["roll"])
                            user.email = data["email"]
                            user.roll = data["roll"]
                            user.username = data["username"]
                            user.country_code = data["country_code"]
                            user.phone_num = data["phone_num"]
                            user.set_password(data["password"])
                            user.save()
                            # sendOTP(user)
                            return JsonResponse({"status": True, "message": "Register Save Succesfully "})
                        else:
                            return JsonResponse({"status": False, "message": "All fields required!"})    
                    else:
                        return JsonResponse({"status": False, "message": "Email allready exits !!!"})    
                else:
                    return JsonResponse({"status": False, "message": "Data format not support !!!"})    
            else:
                return JsonResponse({"status": False, "message": "Something went wrong!"})        
        except:
            return JsonResponse({"status": False, "message": "Something went wrong!"})

class LoginUser(APIView):
    def post(self, request):
        # try:
            data = request.data
            if data:
                serializer = LoginSerializer(data=data)
                if serializer.is_valid():
                    if User.objects.filter(email=data["email"].lower()).exists():
                        user = User.objects.get(email=data["email"].lower())
                        if user.check_password(data["password"]):
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