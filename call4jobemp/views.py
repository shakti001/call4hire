from django.shortcuts import render,redirect
from call4jobapp.models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import MD5PasswordHasher, make_password
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
# Create your views here.
from django.core.files.storage import FileSystemStorage

User = get_user_model()

# AIzaSyCDt3swXLDeZLGJs2NnyUbRvI7m1cpo7iQ
def home(request):
    try:
        job = JobPost.objects.filter(job_status = "Accepted")

        cms_page = Cms_pages.objects.all()
        blog = Blog.objects.all()
        date = datetime.datetime.now()
    except:
        return redirect('/')
    
    return render(request, "call4jobemp/index.html",{'job':job,"cms_page":cms_page,'blog':blog})

def search(request):
    try:
        job = JobPost.objects.filter(job_status = "Accepted")
        job_count = JobPost.objects.filter(job_status = "Accepted").count()
        job_category = JobCategory.objects.all()
        if request.method == "POST":
            skills = request.POST.get("skills")
            exp = request.POST.get("exp")
            location = request.POST.get("location")
            if exp == "10+":
                data = JobPost.objects.filter(skills__contains=skills,job_location__contains=location, minimum_exp__gte=10)
                return render(request, "call4jobemp/job_listing.html", {'data':data,"job":job,'job_category':job_category,'job_count':job_count})
            else:
                data = JobPost.objects.filter(skills__contains=skills,job_location__contains=location, minimum_exp__contains=exp)
                return render(request, "call4jobemp/job_listing.html", {'data':data,"job":job,'job_category':job_category,'job_count':job_count})
    except:
         return redirect('/')


def signup(request):
    return render(request, "call4jobemp/auth/register.html")

def signupAjax(request):
    try:
        if request.method == "POST":
            name= request.POST.get("name") 
            email= request.POST.get("email")
            number= request.POST.get("number")
            password= request.POST.get("password")
            work_status= request.POST.get("work_status")
            employee_address= request.POST.get("address")
            gender= request.POST.get("gender")
            dob = request.POST.get("dob")
            resume= request.FILES.get("resume")
            if name and email and number and  password and work_status and employee_address and gender and dob and resume:
                if User.objects.filter(email = email).exists():
                    return JsonResponse({"status":"error", "message":"Email Allready Exit !!!!"})
                elif User.objects.filter(company_mobile_number = number).exists():
                    return JsonResponse({"status":"error", "message":"Email Allready Exit !!!!"})
                else:
                    user = User.objects.create(username=name, employee_address=employee_address,gender=gender,dob=dob, roll="employee", email=email, company_mobile_number=number, password=make_password(password), work_status=work_status, resume=resume)
                    user.save()
                    return JsonResponse({"status":"success", "message":"Data saved successsfully !!!!","slug":user.slug})
            else:
                return JsonResponse({"status":"error", "message":"Something went wrong !!!!"})

        else:
            return JsonResponse({"status":"error", "message":"Something went wrong !!!!"})
    except:
        return JsonResponse({"status":"error", "message":"Something went wrong !!!!"})
def signupEmployementAjax(request,slug):
    try:
        if request.method == "POST":
            employed_type = request.POST.get('employed_type')
            year = request.POST.get('year')
            month = request.POST.get('month')
            Currentcompany = request.POST.get('Currentcompany')
            Previouscompany = request.POST.get('Previouscompany')
            designation = request.POST.get('designation')
            key_skills = request.POST.get('key_skills')
            work_type = request.POST.get('work_type')
            joiningdate = request.POST.get('joiningdate')
            leaveingdate = request.POST.get('leaveingdate')
            salary = request.POST.get('salary')
            noticeperiod = request.POST.get('noticeperiod')
            
            user = User.objects.get(slug=slug)
            if employed_type == "on":
                data = userEmployementDetails.objects.create(user_id = user.id, current_emp="yes",
                                                            work_exp_year=year, work_exp_month=month,current_company_name=Currentcompany,
                                                            designation=designation,key_skills=key_skills,
                                                            work_type=work_type,joining_date=joiningdate,current_salary=salary,
                                                            notice_period=noticeperiod)
                user.FillEmpstatus = True
                user.save()
                return JsonResponse({"status":"success", "message":"Data saved successsfully !!!!","slug":user.slug})
            else:
                data = userEmployementDetails.objects.create(user_id = user.id, current_emp="no",
                                                            work_exp_year=year, work_exp_month=month,
                                                            pervious_company_name=Previouscompany,designation=designation,key_skills=key_skills,
                                                            work_type=work_type,joining_date=joiningdate,leaving_date=leaveingdate,current_salary=salary,
                                                            notice_period=noticeperiod)
                user.FillEmpstatus = True
                user.save()
                return JsonResponse({"status":"success", "message":"Data saved successsfully !!!!","slug":user.slug})
    except:
        return JsonResponse({"status":"error", "message":"Something went wrong!!!!"})
    return render(request, "call4jobemp/auth/employment-details.html",{'slug':slug})

def login(request):
    try:
        data = request.POST
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            if email and password:
                user = User.objects.filter(email=email).exists()
                if user:
                    checkEmpStatus = User.objects.get(email=email)
                    if  checkEmpStatus.roll == "employee" :
                        if checkEmpStatus.FillEmpstatus == True:
                            loginUser = auth.authenticate(email=email, password=password)
                            if loginUser:
                                auth.login(request, loginUser)
                                messages.success(request, "Login successfully")
                                return redirect("/")
                            else:
                                messages.error(request, "Email Id password does not match")
                                return redirect("/login/")
                        else:
                            messages.error(request, "please fill employement first")
                            return redirect('/signupEmployementAjax/'+str(checkEmpStatus.slug))
                    else:
                        messages.error(request, "Email Id password does not match")
                        return redirect("/login/")   
                else:
                    messages.error(request, "Email Id password does not match")
                    return redirect("/login/")
            else:
                messages.error(request, "Email Id password does not match")
                return redirect("/login/") 
    except:
        return redirect('/')
 
    return render(request, "call4jobemp/auth/login.html",{'data':data})

def logout(request):
    auth.logout(request)
    return redirect("/login/")



def profile(request, slug):
    data = None
    user = None
    try:
        user_id = User.objects.get(slug=slug)
        data = userEmployementDetails.objects.get(user_id = user_id.id)
    except:
        return render(request, "call4jobemp/auth/profile.html", {"data":data, 'user':user_id})

    return render(request, "call4jobemp/auth/profile.html", {"data":data, 'user':user_id})

def profileSkillsSaveAjax(request, slug):
    try:
        user_id = User.objects.get(slug=slug)
        data = userEmployementDetails.objects.get(user_id = user_id.id)
        if request.method == "POST":
            skills = request.POST.get("skills")
            if skills is not None or skills:
                data.key_skills = skills
                data.save()
                return JsonResponse({"status":"status" ,"message":"key skills updated", "slug":slug , "skills":data.key_skills})
    except:
        return redirect('/')

        
    return render(request, "call4jobemp/auth/profile.html")

def UpdateBasicDetailsAjax(request, slug):
    try:
        user = User.objects.get(slug=slug)
        data = userEmployementDetails.objects.get(user_id=user.id)

        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_num = request.POST.get('mobile_num')
            email = request.POST.get('email')
            abilityjoin = request.POST.get('abilityjoin')
            workstatus = request.POST.get('workstatus')
            location = request.POST.get('location')

            if user:
                user.first_name = first_name
                user.last_name = last_name
                user.company_mobile_number = mobile_num
                user.email = email
                user.work_status = workstatus
                user.employee_address = location

                
                user.save()
                if data:
                    data.notice_period = abilityjoin
                    data.save()
                    return JsonResponse({"status":"success", "message":"Profile Update successfully","slug":slug})

                else:
                    return JsonResponse({"status":"error", "message":"Something went wrong"})
            else:
                return JsonResponse({"status":"error", "message":"Something went wrong"})
    except:
        return redirect('/')

    return render(request, "call4jobemp/auth/profile.html")

def updateEmployementAjax(request,slug):
    try:
        if request.method == "POST":
            employed_type = request.POST.get('employed_type')
            year = request.POST.get('year')
            
            month = request.POST.get('month')
            
            Currentcompany = request.POST.get('Currentcompany')
            
            Previouscompany = request.POST.get('Previouscompany')
            
            designation = request.POST.get('designation')
            
            key_skills = request.POST.get('key_skills')
            
            work_type = request.POST.get('work_type')
            skills_used = request.POST.get('skills_used')
            joiningdate = request.POST.get('joiningdate')
            
            leaveingdate = request.POST.get('leaveingdate')
            
            salary = request.POST.get('salary')
            
            noticeperiod = request.POST.get('noticeperiod')
            
            user = User.objects.get(slug=slug)
            data = userEmployementDetails.objects.filter(user_id = user.id).exists()
            if data is not None:

                if employed_type == 'yes':
                    dataSave = userEmployementDetails.objects.filter(user_id = user.id)

                    dataSave.update(
                
                    current_emp='yes',
                    work_exp_year=year, 
                    work_exp_month=month,
                    current_company_name=Currentcompany,
                                                                
                    designation=designation,
                    skills_used = skills_used,
                    work_type=work_type,
                    joining_date=joiningdate,
                    current_salary=salary,
                    notice_period=noticeperiod,
                    )
                    
                    user.FillEmpstatus = True
                    user.save()
                    return JsonResponse({"status":"success", "message":"Data saved successsfully !!!!","slug":user.slug})
                elif employed_type == 'no':
                    dataSave = userEmployementDetails.objects.filter(user_id = user.id)

                    dataSave.update(
                
                    current_emp='no',
                    work_exp_year=year, 
                    work_exp_month=month,
                    pervious_company_name=Previouscompany,
                                                                
                    designation=designation,
                    work_type=work_type,
                    joining_date=joiningdate,
                    leaving_date=leaveingdate,
                    skills_used = skills_used,
                    current_salary=salary,
                    notice_period=noticeperiod,
                    )
                    
                    user.FillEmpstatus = True
                    user.save()
                return JsonResponse({"status":"success", "message":"Data saved successsfully !!!!","slug":user.slug})
            else:
                return JsonResponse({"status":"error", "message":"Something went wrong!!!!"})
    except:
        return JsonResponse({'status':'error', 'message':"something went worng"})
    return render(request, "call4jobemp/auth/employment-details.html",{'slug':slug})

def profileItSkillsSaveAjax(request, slug):
    try:
        user_id = User.objects.get(slug=slug)
        data = userEmployementDetails.objects.get(user_id = user_id.id)

        if request.method == "POST":
            itskills = request.POST.get("itskills")
            if itskills is not None or itskills:
                data.it_skills = itskills
                data.save()
                return JsonResponse({"status":"status" ,"message":"It skills updated", "slug":slug , "skills":data.it_skills})
    except:
        return redirect('/')
    
    return render(request, "call4jobemp/auth/profile.html")

def resumeUpload(request, slug):
    try:
        user_id = User.objects.get(slug=slug)
        data = userEmployementDetails.objects.get(user_id = user_id.id)

        if request.method == "POST":
            resumeUpload = request.FILES.get("resume")
            if resumeUpload is not None or resumeUpload:
                # fs = FileSystemStorage()
                # file = fs.save(resumeUpload.name, resumeUpload)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                # fileurl = fs.url(file)
    
                user_id.resume = resumeUpload
                user_id.save()
            return JsonResponse({"status":"status" ,"message":"key skills updated", "slug":slug})
    except:
        return redirect('/')
    
    return render(request, "call4jobemp/auth/profile.html")

def imgUpload(request, slug):
    try:
        user_id = User.objects.get(slug=slug)
        data = userEmployementDetails.objects.get(user_id = user_id.id)
        if request.method == "POST":
            imgUpload = request.FILES.get("image")
            if imgUpload is not None or imgUpload:
                user_id.image = imgUpload
                user_id.save()
            return JsonResponse({"status":"status" ,"message":"key skills updated", "slug":slug })
    except:
        return redirect('/')
    
    return render(request, "call4jobemp/auth/profile.html")

def viewApplyJobs(request, slug):
    try:
        user = User.objects.get(slug=slug)
        apply_job = ApplyJob.objects.filter(user_id=user.id)
    except:
        return redirect('/')

    return render(request, "call4jobemp/jobs/apply-jobs.html", {'apply_job':apply_job, 'user':user})



# def profileSkillsSaveAjax(request, slug):
#     user_id = User.objects.get(slug=slug)
#     data = userEmployementDetails.objects.get(user_id = user_id.id)
#     if request.method == "POST":
#         Itskills = request.POST.get("Itskills")
#         if Itskills is not None or Itskills:
#             data.it_skills = Itskills
#             data.save()
#             return JsonResponse({"status":"status" ,"message":"key skills updated", "slug":slug , "skills":data.it_skills})
    
#     return render(request, "call4jobemp/auth/profile.html")








def jobDescription(request,slug):
    try:
        job = JobPost.objects.get(slug=slug)
        all_job = JobPost.objects.filter(job_status = "Accepted")
        fetchApplyJob = ApplyJob.objects.filter(user_id = request.user.id , job_id=job.id)
    except:
        return redirect('/')
    return render(request,"call4jobemp/job_details.html",{'job':job,'all_job':all_job,'fetchApplyJob':fetchApplyJob})
    
@login_required(login_url="/login/")
def applyjob(request,slug):
    try:
        job = JobPost.objects.get(slug=slug)
        fetchApplyJob = ApplyJob.objects.filter(user_id = request.user.id , job_id=job.id)
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            
            job_id = request.POST.get('job_id')
            if user_id:
                if user_id and job_id:
                    data = ApplyJob.objects.create(job_id=job_id,user_id=user_id)
                    data.save()
                    messages.success(request , "Job apply successfully !!!! ")
                    return redirect("/job-description/" +str(slug))
                else:
                    messages.error(request , "Something went wrong!!!! ")
                    return redirect("/job-description/" +str(slug))
            else:
                messages.error(request , "Login before apply !!!")
                return redirect("/login/")
    except:
        return redirect('/')
        
        
                
        
       
    return render(request, "call4jobemp/job_details.html",{'job':job,'fetchApplyJob':fetchApplyJob})


def FindJobs(request):
    try:
        request.session['job_cat_id'] = []
    
        if request.method == "POST":
            
            job_cat_id = request.POST.get("job_category")
        
            
            job_type_list = request.POST.getlist("job_type_list[]")
        
            
            job_location = request.POST.get("location")
        
            
            exp = request.POST.get("exp")
            salary = request.POST.getlist("salary_list[]")
        
            
                
            if job_cat_id == "" or job_cat_id == None:
                q = (
                    (Q(job_types__in = job_type_list)) 
                    | Q(job_location__istartswith=job_location) | Q(maximum_exp = exp) | Q(minimum_annual_salary = salary)
                
                
                    )
                
                jobs = JobPost.objects.filter(q , job_status="Accepted" )
                count = jobs.count() 
                print(jobs,"aaaaaaaaaaa")
                return render(request , "call4jobemp/return_job_filter.html", {'job':jobs, 'job_count':count})
            else:
                q = (
                    (Q(job_category_id=job_cat_id) |  Q(job_types__in = job_type_list))
                    | Q(job_location__istartswith=job_location) | Q(maximum_exp = exp) | Q(minimum_annual_salary = salary)
                
                    )
                
                jobs = JobPost.objects.filter(q , job_status="Accepted" )
                
                # job = jobs.filter(job_location__istartswith=job_location)
                
                count = jobs.count()
                print(jobs,"bbbbbbbbbbbbb")
                
                return render(request , "call4jobemp/return_job_filter.html", {'job':jobs,'job_count':count})
        job = JobPost.objects.filter(job_status = "Accepted")
        job_count = JobPost.objects.filter(job_status = "Accepted").count()
        job_category = JobCategory.objects.all()
    except:
        return redirect('/')
    return render(request ,"call4jobemp/job_listing.html",{"job":job,'job_category':job_category,'job_count':job_count})


def about(request):
    try:
        cms = Cms_pages.objects.get(slug="About-us")
    except:
        return redirect('/')
        
    return render(request, "call4jobemp/about.html",{'cms':cms})

def contact(request):
    try:
        if request.method == "POST":
            name= request.POST.get('names')
            message= request.POST.get('messages')
            email= request.POST.get('emails')
            subject= request.POST.get('subjects')
            if name and message and email and subject:
                
            
                data = Contact.objects.create(name= name, message=message, email=email, subject=subject)
                data.save()
                messages.success(request, "Contact sent successfully !!!")
                return redirect("/contact/")
            else:
                messages.error(request, "All fields are required !!!")
                return redirect("/contact/")
    except:
        messages.error(request, "Something went wrong!!!")
        return redirect("/contact/")
     
    return render(request, "call4jobemp/contact.html")

def blogDetails(request,slug):
    try:
        blog = Blog.objects.get(slug=slug)
        blogcat = BlogCategory.objects.all()
    except:
        messages.error(request, "Something went wrong!!!")
        return redirect("/")
    return render(request, "call4jobemp/single-blog.html",{'blog':blog,'blogcat':blogcat})

def aboutMobile(request):
    try:
        cms = Cms_pages.objects.get(slug="About-us")
    except:
        return redirect('/')
    return render(request, "call4jobemp/aboutformob.html",{'cms':cms})