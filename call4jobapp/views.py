from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from .helpers import *
from django.contrib.auth.hashers import MD5PasswordHasher, make_password
from django.contrib.auth import authenticate, login as login_check
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
User = get_user_model()

@login_required(login_url="/")
def home(request):
    return render(request, "call4job/home/index.html")

def signup(request):
    if request.method=="POST":
        company_email = request.POST.get("email")
        adhar_card = request.POST.get("adhar_card")
        pan_card = request.POST.get("pan_card")
        company_gst = request.POST.get("cgst")
        company_name = request.POST.get("cname")
        company_mobile_num = request.POST.get("cnum")
        company_address = request.POST.get("caddress")
        image = request.POST.get("cimage")

        user_type = request.POST.get("user_type")
        password =  generatePassword()
        if User.objects.filter(email=company_email):
            messages.error(request, "Email Allready Exits")
            return redirect('/company/signup/')
        elif User.objects.filter(company_mobile_number=company_mobile_num):
            messages.error(request, "Mobile Number Allready Exits")
            return redirect('/company/signup/')
        else:
            data = User.objects.create(email = company_email, image=image,  password=make_password(password),adhaar_card=adhar_card,pan_card=pan_card,company_gst=company_gst,company_mobile_number=company_mobile_num,company_name=company_name, roll=user_type,company_address=company_address)
            send_to = [company_email]
            subject = "Your Password is Here "
            content = (
                "Hi"
                + "" +company_name
                + "Welcome on Call4job"
                
                + " Your Zenerated Password is  "
                + password
            )
            sendMail(subject, content, send_to)
            # sendSMS(data , company_mobile_num)
            messages.success(request, "Your account has been created please login")
            return redirect('/company/')
    return render(request, "call4job/auth/signup.html")

def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(email=email).exists():
            user = auth.authenticate(email=email, password=password)
            if user is None:
                messages.error(request, "Invalid username or password ")
                return redirect("/company/")
            elif user:
                if user.user_status == "0":
                    messages.error(request, "Your Acoount is in under verification. ")
                    return redirect("/company/")
                elif user.user_status == "2":
                    messages.error(request, "Your Acoount is suspended.please contact admin ")
                    return redirect("/company/")
                else:
                    auth.login(request, user)
                    messages.success(request, "Login successfully")
                    return redirect("/company/home/")
            else:
                messages.error(request, "Invalid username or password ")
                return redirect("/company/")
        else:
            messages.error(request, "Invalid username or password ")
            return redirect("/company/")
    return render(request, "call4job/auth/login.html")

def forgotPassword(request):
    if request.method=="POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.roll == "Company":
                otp = generateOTP()
                user.Otp = otp
                user.save()
                send_to = [email]
                subject = "ONE TIME PASSOWRD"
                content = (
                    "Hi"
                    + "" + user.company_name
                    + "Your ONE TIME PASSWORD is"
                    + otp
                )
                sendMail(subject, content, send_to)
                messages.success(request,"Please Enter Otp Here.")
                return redirect("/company/otp-verify/"+str(user.slug))
            else:
                messages.error(request, "Email not found !!!")
                return redirect('/company/forgot-password/')
        else:
            messages.error(request, "Email not found !!!")
            return redirect('/company/forgot-password/')

    return render(request,"call4job/auth/forgotpassword.html")

def otp_verify(request, slug):
    if request.method == "POST":
        otp = request.POST.get('otp')
        user = User.objects.get(slug=slug)
        if otp:
            if otp == user.Otp:
                user.Otp = ""
                user.save()
                messages.success(request, "Please enter new password !!!")
                return redirect("/company/forgot-password-form/" + str(user.slug))
            else:
                messages.error(request, "Otp does not match !!!")
                return redirect('/company/otp-verify/'+str(user.slug))
        else:
            messages.error(request, "Please enter Otp  !!!")
            return redirect('/company/otp-verify/'+str(user.slug))
    return render(request,"call4job/auth/otp-verify.html")
    
def forgotPasswordForm(request, slug):
    if request.method == "POST":
        newpassword = request.POST.get("npassword")
        confirmnewpassword = request.POST.get("cnpassword")
        user = User.objects.get(slug=slug)
        if newpassword and confirmnewpassword:
            if newpassword == confirmnewpassword:
                user.password = make_password(newpassword)
                user.save()
                print("password matcheddddddddd")

                messages.success(request, "Password changed Successfully !!!")
                return redirect("/company/")
            else:
                messages.error(request, "Password does not matched !!!")
                return redirect("/company/forgot-password-form/" + str(user.slug))
        else:
            messages.error(request, "Please enter Newpassword !!!")
            return redirect("/company/forgot-password-form/" + str(user.slug))
    return render(request,"call4job/auth/forgotpasswordform.html")

@login_required(login_url="/company/")
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url="/company/")
def edit_profile(request,slug):
    user = User.objects.get(slug = slug)
    if request.method == "POST":
        name = request.POST.get('name')
        mobile_number = request.POST.get('mob_num')
        address = request.POST.get('address')
        print(address,"qqqqqqqqqq")
        if name and mobile_number and address:
            user.username = name
            user.company_mobile_number = mobile_number
            user.company_address = address
            user.save()
            messages.success(request,"Profile save successfully !!! ")
            return redirect("/company/edit-profile/" + str(slug))
        else:
            messages.error(request,"All fileds required !!! ")
            return redirect("/company./edit-profile/" + str(slug))
            
    return render(request, "call4job/profile/profile.html",{'user':user})

 
def change_password(request, slug):
    if request.method == "POST":
        password = request.POST.get("pass")
        new_passowrd = request.POST.get("newpass")
        rnew_passowrd = request.POST.get("cnewpass")
        user = User.objects.get(slug=slug)

        check = user.check_password(password)
        if check == True:
            if new_passowrd == rnew_passowrd:
                user.set_password(new_passowrd)
                user.save()
                user = User.objects.get(id=user.id)
                login_check(request, user)
                messages.success(request, " Password changed Successfully !!!! ")
                return redirect("/company/change-password/" + str(slug))
            else:
                messages.error(request, " Password Does not Match !!!! ")
                return redirect("/company/change-password/" + str(slug))
        else:
            messages.error(request, " Old password Does not Match !!!! ")
            return redirect("/company/change-password/" + str(slug))
    return render(
        request, "call4job/profile/change-password.html"
    )



def jobCategory(request):
    job = JobCategoryCompany.objects.filter(user_id = request.user.id)
    return render(request, "call4job/jobs/job-category/jobcategory.html",{"job":job})



# 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

def add_category(request):
    if request.method=="POST":
        user_id = request.POST.get("user_id")
        print(user_id,"user_id")        
        count = request.POST.get("count")
        print(count,"aaaaaaaa")
        category_name = request.POST.get("category_name")
        print(category_name,"aaaaaaaa")
        
        if user_id and category_name:
            data = JobCategoryCompany.objects.create(user_id = user_id, name=category_name)
            data.save()  
        if count:
            c = int(count)
            i = 1
            while 0 < c:
                print(i,"addd iiiiiiii")
                category_option = request.POST.get(f"category_option_{i}")
                option_data = JobCategoryOptionCompany.objects.create(name=category_option, job_category_id = data.id)
                option_data.save()
                break
            messages.success(request, "CXategory & option create successfully  !!!!")
            return redirect("/company/category/")
                
        else:
            messages.error(request, "Please fill category name  !!!!")
            return redirect("/company/add-category/")
            
        
       
    return render(request, "call4job/jobs/job-category/add_category.html")


def edit_category(request,slug):
    category = JobCategoryCompany.objects.get(slug=slug)
    categoryOption = JobCategoryOptionCompany.objects.filter(job_category_id=category.id)
    
    if request.method=="POST":
        user_id = request.POST.get("user_id")
        print(user_id,"user_id")
        
        count = request.POST.get("count")
        print(count,"count")
        
        category_name = request.POST.get("category_name")
        print(category_name,"category_name")
        
        if user_id and category_name:
           category.name = category_name
           category.save()
        if count:
            option_data = JobCategoryOptionCompany.objects.filter(job_category_id = category.id)
            option_data.delete()
            c = int(count)
            i = 1
            for i in range(i, c):
                    option_data = JobCategoryOptionCompany.objects.create(name=category_option, job_category_id = category.id)
                    option_data.save()
            messages.success(request, "Category & option Update successfully  !!!!")
            return redirect("/company/category/")
                
        else:
            messages.error(request, "Please fill category name  !!!!")
            return redirect("/company/add-category/")
            
        
    categoryOption_count = JobCategoryOptionCompany.objects.filter(job_category_id=category.id).count()
    
    return render(request, "call4job/jobs/job-category/edit_category.html",{'category':category,'categoryOption':categoryOption,'range_categoryOption_count':range(categoryOption_count),'categoryOption_count':categoryOption_count})



# def edit_category(request, slug):
#     category = JobCategory.objects.get(slug=slug)
#     if request.method=="POST":
#         category_name = request.POST.get("category_name")
#         if category_name:
#             category.name = category_name
#             category.save()
#             messages.success(request, "Job edited successfully !!!!")
#             return redirect("/admin/job-category/")
#         else:
#             messages.error(request, "Please fill job name !!!!")
#             return redirect("/admin/edit-category/" + str(slug))
#     return render(request, "admin/jobs/job-category/edit_category.html",{'category':category})
 
# def delete_category(request, slug):
#     job = JobCategory.objects.get(slug=slug)
#     job.delete()
#     messages.success(request, "Job  deleted successfully !!!")
#     return redirect('/admin/job-category')


@login_required(login_url="/company/")
def joblist(request):
    job = JobPost.objects.filter(user_id= request.user.id)
    return render(request, "call4job/jobs/joblist.html",{'job':job})

@login_required(login_url="/company/")
def create_job(request):
    if request.method == "POST":
        job_title = request.POST.get('job_title')
        min_exp = request.POST.get('min_exp')
        max_exp = request.POST.get('max_exp')
        min_ctc = request.POST.get('min_ctc')
        max_ctc = request.POST.get('max_ctc')
        no_of_emp = request.POST.get('no_of_emp')
        higher_edu = request.POST.get('higher_edu')
        work_place = request.POST.get('work_place')
        job_type = request.POST.get('job_type')
        job_description = request.POST.get('job_description')
        skills = request.POST.get('skills')
        salary = request.POST.get('salary')
        job_category = request.POST.get('job_category')

        age_criteria = request.POST.get('age_criteria')

        emp_gender = request.POST.get('emp_gender')

        notice_period = request.POST.get('notice_period')

        job_opportunity = request.POST.get('job_opportunity')


        
        if job_title and min_exp and max_exp and min_ctc and no_of_emp and max_ctc and higher_edu and work_place and job_type and job_description and skills and salary and age_criteria and notice_period and job_opportunity and emp_gender:
            user_id = request.user
            data = JobPost.objects.create(user_id = user_id.id, job_category_id = job_category,no_of_emplyoee=no_of_emp, job_types=job_type,work_place=work_place,job_title=job_title,minimum_exp=min_exp,maximum_exp=max_exp, minimum_annual_salary=min_ctc, maximum_annual_salary =max_ctc, company_name=user_id.company_name,job_location=user_id.company_address,higher_education=higher_edu,job_description=job_description,skills=skills,
                                          emp_gender =emp_gender,notice_period = notice_period,job_opportunity = job_opportunity,salary = salary,age_criteria = age_criteria)
            data.save()
            messages.success(request, "Job create successfully !!")
            return redirect('/company/job-list/')
        else:
            user_id = request.user
            messages.error(request, "all fields required")
            return redirect('/company/create-job/')
    job_category = JobCategory.objects.all()
    return render(request, "call4job/jobs/create-job.html", {'job_category':job_category})

@login_required(login_url="/company/")
def edit_job(request , slug):
    job = JobPost.objects.get(slug=slug) 
    if request.method == "POST":
        job_title = request.POST.get('job_title')
        min_exp = request.POST.get('min_exp')
        max_exp = request.POST.get('max_exp')
        min_ctc = request.POST.get('min_ctc')
        max_ctc = request.POST.get('max_ctc')
        no_of_emp = request.POST.get('no_of_emp')
        higher_edu = request.POST.get('higher_edu')
        work_place = request.POST.get('work_place')
        job_type = request.POST.get('job_type')
        job_description = request.POST.get('job_description')
        job_category = request.POST.get('job_category')
        salary = request.POST.get('salary')
        
        skills = request.POST.get('skills')
        
        age_criteria = request.POST.get('age_criteria')

        emp_gender = request.POST.get('emp_gender')

        notice_period = request.POST.get('notice_period')

        job_opportunity = request.POST.get('job_opportunity')
        if job_title and min_exp and salary and age_criteria and emp_gender and  notice_period and job_opportunity and max_exp and min_ctc and max_ctc and higher_edu and work_place and job_type and job_description and skills:
            job.job_title = job_title
            job.minimum_exp = min_exp
            job.maximum_exp = max_exp
            job.minimum_annual_salary = min_ctc
            job.maximum_annual_salary = max_ctc
            job.higher_education = higher_edu
            job.work_place = work_place
            job.job_types = job_type
            job.job_description = job_description
            job.skills = skills
            job.no_of_emplyoee = no_of_emp
            job.job_category_id = job_category
            job.salary = salary
            job.age_criteria = age_criteria
            job.emp_gender = emp_gender
            job.notice_period = notice_period

            job.save()
            messages.success(request, "Job update successfully !!!")
            return redirect('/company/job-list/')
        else:
            messages.error(request, "all fields required")
            return redirect('/company/edit-job/' + str(slug))
    job_category = JobCategory.objects.all()
    
    return render(request, "call4job/jobs/edit-job.html",{'job':job , "job_category":job_category})

@login_required(login_url="/company/")
def delete_job(request, slug):
    instance = JobPost.objects.get(slug=slug)
    instance.delete()
    messages.error(request, " Job deleted successfullyv !!!! ")
    return redirect("/company/job-list/")

@login_required(login_url="/company/")
def view_job(request, slug):
    job = JobPost.objects.get(slug=slug)
    return render(request, "call4job/jobs/view-job.html",{'job':job})

def save_google_type_user(request):
    if request.method=="POST":
        usertype=request.POST.get("user_type")
        request.session['user_type'] = usertype
        return JsonResponse(({"status":"success"}))
    return JsonResponse({"status":"success", "message":"Doneeeee"})
    

def apply_job_listing(request):
    # print(request.user,"aaaaaaaaaa")
    data = ApplyJob.objects.filter( user_id = request.user.id)
    # print(data,"qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
    return render(request, "call4job/jobs/apply-job.html",{'data':data})