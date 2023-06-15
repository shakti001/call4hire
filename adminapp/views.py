from django.shortcuts import render,redirect
from call4jobapp.models import *
from django.contrib.auth import authenticate, login as login_check
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from call4jobapp.helpers import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import MD5PasswordHasher, make_password
from django.contrib.contenttypes.models import ContentType   
from django.contrib.auth.models import Group, Permission
import calendar
from collections import Counter

User = get_user_model()

# Create your views here.
def home(request):
    compaies_count = User.objects.filter(roll="Company").count()
    
    employee_count = User.objects.filter(roll="employee").count()
    apply_employee_count = ApplyJob.objects.all()
    job_count = JobPost.objects.all().count()
    
    user_list = []
    for i in apply_employee_count:
        user_list.append(i.user_id)
    d = Counter(user_list)
    new_user_list = list([item for item in d if d[item]>1])
    count_apply_user = len(new_user_list) 
    employer_query = f"""
        select id, count(*) as total,strftime("%%m",created_at) as month 
        from call4jobapp_user where roll="Company" group by strftime("%%m",created_at);

    """
    employer_user_count = User.objects.raw(employer_query)

    applicant_query = f"""
                select id, count(*) as total,strftime("%%m",created_at) as month 
                from  call4jobapp_user where roll="employee"  group by strftime("%%m",created_at);
            """
    applicant_user_count = User.objects.raw(applicant_query)

    i = 0
    append_in_month_name = []
    employer_data = []
    while i <= 11:
        i += 1

        obj = dict()
        obj.update(
            {"employer_total": 0, "month": calendar.month_name[i], "applicant_total": 0}
        )
        convert_in_month_name = calendar.month_name[i]
        employer_data.append(obj)
    for user in employer_user_count:
        employer_data[int(user.month) - 1]["employer_total"] = user.total

    for user in applicant_user_count:
        employer_data[int(user.month) - 1]["applicant_total"] = user.total
    context = {
        "employer_data": employer_data,
        "compaies_count":compaies_count,
        "employer_user_count": employer_user_count,
        "employee_count":employee_count,
        "apply_employee_count":apply_employee_count,
        "count_apply_user":count_apply_user,
        "job_count":job_count
    }
    return render(request,"admin/home/index.html",context)

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
            user = auth.authenticate(email=email, password=password)
            if user is None:
                messages.error(request, "Invalid email & passsword")
                return redirect('/admin')
            elif user.is_superuser == True:
                messages.success(request, "Welcome in Adminpanel")

                auth.login(request, user)
                return redirect("/admin/home/")
            elif user.roll == "Subadmin":
                auth.login(request, user)
                return redirect("/admin/home/")

            else:
                messages.error(request, "Invalid email & passsword")
                return redirect('/admin')
        else:
            messages.error(request, "Invalid email & passsword")
            return redirect('/admin')
    return render(request,"admin/auth/login.html")

def forgotPassword(request):
    if request.method=="POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_superuser == True:
                otp = generateOTP()
                user.Otp = otp
                user.save()
                send_to = [email]
                subject = "ONE TIME PASSOWRD"
                content = (
                    "Hi Superadmin "
                    + "Your ONE TIME PASSWORD is"
                    + otp
                )
                sendMail(subject, content, send_to)
                messages.success(request,"Please Enter Otp Here.")
                return redirect("/admin/otp-verify/"+str(user.slug))
            elif user.roll == "Subadmin":
                otp = generateOTP()
                user.Otp = otp
                user.save()
                send_to = [email]
                subject = "ONE TIME PASSOWRD"
                content = (
                    "Hi Superadmin "
                    + "Your ONE TIME PASSWORD is"
                    + otp
                )
                sendMail(subject, content, send_to)
                messages.success(request,"Please Enter Otp Here.")
                return redirect("/admin/otp-verify/"+str(user.slug))
                
            else:
                messages.error(request, "Email not found !!!")
                return redirect('/admin/forgot-password/')
        else:
            messages.error(request, "Email not found !!!")
            return redirect('/admin/forgot-password/')
    return render(request,"admin/auth/forgotpassword.html")

def otp_verify(request, slug):
    if request.method == "POST":
        otp = request.POST.get('otp')
        user = User.objects.get(slug=slug)
        if otp:
            if otp == user.Otp:
                user.Otp = ""
                user.save()
                messages.success(request, "Please enter new password !!!")
                return redirect("/admin/forgot-password-form/" + str(user.slug))
            else:
                messages.error(request, "Otp does not match !!!")
                return redirect('/admin/otp-verify/'+str(user.slug))
        else:
            messages.error(request, "Please enter Otp  !!!")
            return redirect('/admin/otp-verify/'+str(user.slug))
    return render(request,"admin/auth/otp-verify.html")
    
def forgotPasswordForm(request, slug):
    if request.method == "POST":
        newpassword = request.POST.get("npassword")
        confirmnewpassword = request.POST.get("cnpassword")
        user = User.objects.get(slug=slug)
        if newpassword and confirmnewpassword:
            if newpassword == confirmnewpassword:
                user.password = make_password(newpassword)
                user.save()
                messages.success(request, "Password changed Successfully !!!")
                return redirect("/admin/")
            else:
                messages.error(request, "Password does not matched !!!")
                return redirect("/admin/forgot-password-form/" + str(user.slug))
        else:
            messages.error(request, "Please enter Newpassword !!!")
            return redirect("/admin/forgot-password-form/" + str(user.slug))
    return render(request,"admin/auth/forgotpasswordform.html")

@login_required(login_url="/admin")
def logout(request):
    auth.logout(request)
    return redirect("/admin/")

@login_required(login_url="/admin/")
def userlist(request):
    user = User.objects.filter(roll="Company", soft_del_status = False).order_by('-created_at')
    return render(request,"admin/users/userlist.html",{'user':user})

@login_required(login_url="/admin/")
def add_userlist(request):
    if request.method == "POST":
        company_email = request.POST.get("company_email")
        adhar_card = request.POST.get("adhaar_card")
        pan_card = request.POST.get("pan_card")
        company_gst = request.POST.get("cgst")
        company_name = request.POST.get("cname")
        company_mobile_num = request.POST.get("cnumber")
        company_address = request.POST.get("caddress")
        company_image = request.POST.get("company_image")

        
        password =  generatePassword()
        
        if company_email and  company_name and adhar_card and pan_card and company_gst  and company_mobile_num and company_address:
            if User.objects.filter(email=company_email).exists():
                messages.error(request, "Email Allready exits  !!!")
                return redirect("/admin/userlist/")
            else:
                
                data = User.objects.create(email=company_email, image=company_image, password=make_password(password), roll="Company", company_mobile_number =company_mobile_num,company_name=company_name,adhaar_card=adhar_card, pan_card=pan_card,company_gst=company_gst,company_address=company_address)
                data.save()
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
                messages.success(request, "User Created Successfully !!!")
                return redirect("/admin/userlist/")
                
        else:
            messages.error(request,"noooodata")
    return render(request,"admin/users/add-user.html")


@login_required(login_url="/admin/")
def edit_userlist(request,slug):
    user = User.objects.get(slug=slug)
    if request.method == "POST":
        # company_email = request.POST.get("company_email")
        adhar_card = request.POST.get("adhaar_card")
        pan_card = request.POST.get("pan_card")
        company_gst = request.POST.get("cgst")
        # company_name = request.POST.get("cname")
        company_mobile_num = request.POST.get("cnumber")
        company_address = request.POST.get("caddress")
        if   adhar_card and pan_card and company_gst  and company_mobile_num and company_address:
            # user.email = company_email
            user.adhaar_card = adhar_card
            user.pan_card = pan_card
            user.company_gst = company_gst
            # user.company_name = company_name
            user.company_mobile_number = company_mobile_num
            user.company_address = company_address
            user.save()
            return redirect("/admin/userlist/")
        else:
            messages.error(request,"noooodata")
    return render(request,"admin/users/edit-user.html",{'user':user})

@login_required(login_url="/admin/")
def delete_userlist(request, slug):
    instance = User.objects.get(slug=slug)
    instance.soft_delete()
    messages.error(request, " user deleted successfully !!!! ")
    return redirect("/admin/userlist/")

def view_userlist(request, slug):
    user = User.objects.get(slug=slug)
    return render(request, "admin/users/view-user.html",{'user':user})

def userStatusAjax(request, user_id):
    if request.method == "POST":
        status = request.POST.get("select")
        
        x = User.objects.get(id=user_id)
        email = x.email
        if x.roll == 'Company':
            ob = User.objects.filter(id=user_id).update(user_status=status)
        # e = email_templates.objects.get(id=2)
        # content = e.content
        # html_page = urllib2.urlopen(url)
            if status == "0":
                send_to = [email]
                subject = "call4hire update your account"
                content = "Your account status is in underverification"
                # name = x.fname + " " + x.lname
    
                # user_status = "Hold"
                # t = strip_tags(content)
                # c = t.replace("{name}", name)
                # msg = c.replace("{LINK}", user_status)
                sendMail(subject, content, send_to)
                return JsonResponse(
                    {"status": "success", "message": "Status changed successfully !!!!"},
                    status=200,
                )
    
            elif status == "1":
                send_to = [email]
                subject = "call4hire update your account"
                content = "Your account status has been Approved"
                sendMail(subject, content, send_to)
                return JsonResponse(
                    {"status": "success", "message": "Status changed successfully !!!!"},
                    status=200,
                )
            else:
                send_to = [email]
                subject = "call4hire update your account"
                content = "Your account status has been Suspended.Please contact admin"
                sendMail(subject, content, send_to)
                return JsonResponse(
                    {"status": "success", "message": "Status changed successfully !!!!"},
                    status=200,
                )
        else:
            ob = User.objects.filter(id=user_id).update(user_status=status)
            return JsonResponse(
                    {"status": "success", "message": "Status changed successfully !!!!"},
                    status=200,
                )
    else:
        return JsonResponse(
            {"status": "error", "message": "Status changed successfully !!!!"},
            
        )


def empList(request):
    user = User.objects.filter(roll="employee", soft_del_status=False).order_by('-created_at')
    return render(request,"admin/users/employee/employee_list.html",{'user':user})

def view_empList(request, slug):
    try:
        user = User.objects.get(slug=slug)
        user_employementDetails = userEmployementDetails.objects.get(user_id = user.id)
        urlObject = request.get_host()
        return render(request, "admin/users/employee/view-emp.html",{'user':user, 'urlObject':urlObject,'user_employementDetails':user_employementDetails})
    except:
        messages.error(request, "Employment details not found !! Please Update Employement details !!!")
        return redirect("/admin/employeeList/")

def delete_emplist(request, slug):
    instance = User.objects.get(slug=slug)
    # instance.delete()
    instance.soft_delete()
    messages.error(request, " Employee deleted successfullyv!!!! ")
    return redirect("/admin/employeeList/")


@login_required(login_url="/admin/")
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
            return redirect("/admin/edit-profile/" + str(slug))
        else:
            messages.error(request,"All fileds required !!! ")
            return redirect("/admin/edit-profile/" + str(slug))
            
    return render(request, "admin/profile/profile.html",{'user':user})
   
def change_password(request, slug):
    if request.method == "POST":
        password = request.POST.get("pass")
        print(password)
        new_passowrd = request.POST.get("newpass")
        rnew_passowrd = request.POST.get("cnewpass")
        user = User.objects.get(slug=slug)

        check = user.check_password(password)
        if check == True:
            if new_passowrd == rnew_passowrd:
                user.set_password(new_passowrd)
                user.save()
                auth.login(request, user)
                messages.success(request, " Password changed Successfully !!!! ")
                return redirect("/admin/change-password/" + str(slug))
            else:
                messages.error(request, " Password Does not Match !!!! ")
                return redirect("/admin/change-password/" + str(slug))
        else:
            messages.error(request, " Old password Does not Match !!!! ")
            return redirect("/admin/change-password/" + str(slug))
    return render(
        request, "admin/profile/change-password.html"
    )

def joblist(request):
    job_id_list = []
    user_id_list = []
   
    job = JobPost.objects.all()
    getJobId = Assign_job.objects.filter(job_id__in=job)
    for i in getJobId:
        job_id_list.append(i.job_id)
        user_id_list.append(i.user_id)
        
        # print(i.id,'qqqqqqqq')
    user = User.objects.filter(roll="Subadmin")
    
    return render(request,"admin/jobs/joblist.html",{'job':job,'user':user,"job_id_list":job_id_list,'user_id_list':getJobId})

def add_joblist(request):
    user = User.objects.filter(roll="Company")
    if request.method == "POST":
        company_id = request.POST.get('company_name')

        job_title = request.POST.get('job_title')
        min_exp = request.POST.get('min_exp')
        max_exp = request.POST.get('max_exp')
        min_ctc = request.POST.get('min_ctc')
        max_ctc = request.POST.get('max_ctc')
        no_of_emp = request.POST.get('no_of_emp')
        higher_edu = request.POST.get('higher_edu')
        work_place = request.POST.get('work_place')
        
        job_type = request.POST.get('job_type')
        job_category = request.POST.get('job_category')
        
        job_description = request.POST.get('job_description')
        skills = request.POST.get('skills')
        
        if job_title and min_exp and max_exp and min_ctc and no_of_emp and max_ctc and higher_edu and work_place and job_type and job_description:
            user = User.objects.get(id=company_id)
            data = JobPost.objects.create(user_id = company_id, job_category_id = job_category, company_name=user.company_name, job_location=user.company_address, no_of_emplyoee=no_of_emp, job_types=job_type,work_place=work_place,job_title=job_title,minimum_exp=min_exp,maximum_exp=max_exp, minimum_annual_salary=min_ctc, maximum_annual_salary =max_ctc,higher_education=higher_edu,job_description=job_description)
            data.save()
            messages.success(request, "Job create successfully !!")
            return redirect('/admin/job-list/')
        else:
            messages.error(request, "Fill all fileds!!")
            return redirect('/admin/add-joblist/')
    job_category = JobCategory.objects.all()
    return render(request, "admin/jobs/add_job.html",{'user':user,'job_category':job_category})

def edit_joblist(request,slug):
    user = User.objects.filter(roll="Company")
    job_category = JobCategory.objects.all()

    
    data = JobPost.objects.get(slug=slug)
    if request.method == "POST":
        company_id = request.POST.get('company_name')
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
        
        skills = request.POST.get('skills')
        if job_title and min_exp and max_exp and min_ctc and no_of_emp and max_ctc and higher_edu and work_place and job_type and job_description and skills:
            user = User.objects.get(id=company_id)
            data.user_id = company_id
            data.company_name = user.company_name
            data.job_location = user.company_address
            data.no_of_emplyoee = no_of_emp
            data.job_title = job_title
            data.min_exp = min_exp
            data.max_exp = max_exp
            data.min_ctc = min_ctc
            data.higher_education = higher_edu
            data.work_place = work_place
            data.job_types = job_type
            data.job_description = job_description
            data.skills = skills
            data.job_category_id = job_category
            data.save()
            messages.success(request, "Job create successfully !!")
            return redirect('/admin/job-list/')
    return render(request, "admin/jobs/edit-job.html",{'user':user,'data':data,'job_category':job_category})

def delete_joblist(request, slug):
    job = JobPost.objects.get(slug=slug)
    job.delete()
    messages.success(request,"Job deleted updated !!!!!")

    return redirect("/admin/job-list/")

def view_joblist(request, slug):
    job = JobPost.objects.get(slug=slug)
    return render(request, "admin/jobs/view-job.html",{'job':job})

def company_user_ajax(request):
    if request.method == "POST":
        select = request.POST.get('select')
        user = User.objects.get(id=select)
        return JsonResponse({'status':'success', 'message':"doneeee", "location":user.company_address})
    return render(request, "admin/jobs/add_job.html")

def job_status_ajax(request , id): 
    if request.method == "POST":
        job_status = request.POST.get("job_status")        
        job = JobPost.objects.get(id=id)
        job.job_status = job_status
        job.save()
        return JsonResponse({'status':'success',"message":"Job changed successfully !!!"})
    return render(request, "admin/jobs/joblist.html",)

def assign_job__ajax(request , id):
    
    if request.method == "POST":
        user = request.POST.get("assign_user")
        
        if Assign_job.objects.filter(job_id = id).exists():
            return JsonResponse({"status":"error" , "message":"Job allready assigned"})
        else:
            data = Assign_job.objects.create(user_id = user, job_id=id)
            data.save()
            
            return JsonResponse({'status':'success',"message":"Job Assign successfully !!!"})
    return render(request, "admin/jobs/joblist.html",)

def add_subadmin(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_num = request.POST.get('number')
        role = request.POST.get('roll')
        password =  generatePassword()
        job_category = request.POST.get('job_category')
        permission = request.POST.getlist("name[]")
        if  name and email and mobile_num and  role:
            if User.objects.filter(email=email).exists():
                messages.error(request,"all fields required !!!!!")
                return redirect("/admin/add-subadmin/")
            else:
                data = User.objects.create(username=name, job_category_id=job_category, password = make_password(password),roll=role,email=email,company_mobile_number=mobile_num)
                data.save()
                send_to = [email]
                subject = "Your Password is Here "
                content = (
                    "Hi"
                    + "" + name 
                    + "Welcome on Call4job"
                    
                    + " Your Zenerated Password is  "
                    + password
                )
                sendMail(subject, content, send_to)        
                for i in permission:
                    print(i,"qqq")
                    per = User.objects.get(id=data.id)
                    per.user_permissions.add(i)
                    
                # user = User.objects.get(id=data.id)
                # user.user_permissions.add(i)
                messages.success(request, "Subadmin created successfully !!!!")

                return redirect('/admin/subadmin/')
        else:
            messages.error(request,"all fields required")
            return redirect('/admin/add-subadmin/')
    else:
        job_category = JobCategory.objects.all()
        
        userdata = User.objects.all()
        content = ContentType.objects.all()
        
        model_list = [
            "dashboard",
            "jobpost",
            "user",
            "subadmin",
            "assign_job",
            "jobcategory",
            "cms_pages",
            "blog"
            
        ]
        

        list_1 = list()
        for i in content:
            
            if i.model in model_list:
                
                list_1.append(i.id)
            else:
                pass
        list_2 = list()
        for i in list_1:
            per = Permission.objects.filter(content_type_id=i)
            x = list()
            c = 1
            for i in per:
                if c == 1:
                    s_name = i.content_type.model.split("_")
                    if len(s_name) > 1:
                        s = ""
                        for name in s_name:
                            if name == 0:
                                s = name.title()
                            else:
                                s = s + " " + name.title()
                        x.append(s)
                    else:
                        x.append(s_name[0].title())
                    c += 1
                else:
                    pass

                if "sidebar" in i.name:
                    x.insert(1, {"Sidebar": i.id})
                if "view" in i.name:
                    x.append({"View": i.id})
                if "add" in i.name:
                    x.append({"Add": i.id})
                elif "change" in i.name:
                    x.append({"Edit": i.id})
                elif "delete" in i.name:
                    x.append({"Delete": i.id})
                

            try:
                list_2.append(x)
            except:
                pass
        return render(request, "admin/subadmin/add-subadmin.html", {"list_2": list_2, "userdata": userdata, "job_category":job_category })
        # return render(request, "subadmin/add.html",)
    # except:
    #     messages.error(request, " Subadmin is created Failed !")
    #     return redirect("/admin/subadmin/add")
    # return render(request, "admin/subadmin/add-subadmin.html")

def subadmin(request):
    user = User.objects.filter(roll="Subadmin")
    return render(request, "admin/subadmin/subadmin.html", {'user':user})

def edit_subadmin(request,slug):
    if request.method == "POST":
        name = request.POST.get('name')
        # email = request.POST.get('email')
        mobile_num = request.POST.get('number')
        job_category = request.POST.get('job_category')
        
        permission = request.POST.getlist("name[]")
        # role = request.POST.get('roll')
        if  name and mobile_num :
            data = User.objects.get( slug=slug)         
            data.username= name
            # data.email= email
            data.company_mobile_number= mobile_num
            data.roll = "Subadmin"
            data.job_category_id = job_category
            data.save()
            data.user_permissions.clear()
            for i in permission:
                user = User.objects.get(slug=slug)
                user.user_permissions.add(i)
            messages.success(request, "Subadmin created successfully !!!!")
            return redirect('/admin/subadmin/')
        else:
            messages.error(request, "All fields Required !!!!")
            return redirect('/admin/edit-subadmin/'+ str(slug))
    else:
        users = User.objects.filter(slug=slug)
        userdata = User.objects.all()
        job_category = JobCategory.objects.all()
        
        try:
            u = User.objects.get(slug=slug)
        except:
            messages.error(request, " Subadmin is created Failed !")
            return redirect("/admin/edit_subadmin/" + slug)

        c = ContentType.objects.all()
        model_list = [
             "dashboard",
            "jobpost",
            "user",
            "subadmin",
            "assign_job",
            "jobcategory",
            "cms_pages",
            "blog"
            
            
        ]
        list_1 = []
        for i in c:
            if i.model in model_list:
                list_1.append(i.id)
            else:
                pass
        l1 = []
        for i in list_1:
            per = Permission.objects.filter(content_type_id=i)
            x = []
            c = 1
            for i in per:
                if c == 1:
                    s_name = i.content_type.model.split("_")
                    if len(s_name) > 1:
                        s = ""
                        for name in s_name:
                            if name == 0:
                                s = name.title()
                            else:
                                s = s + " " + name.title()
                        x.append(s)
                    else:
                        x.append(s_name[0].title())

                    c += 1
                else:
                    pass
                if "sidebar" in i.name:
                    x.insert(1, {"Sidebar": i.id})
                elif "view" in i.name:
                    x.append({"View": i.id})
                elif "add" in i.name:
                    x.append({"Add": i.id})
                elif "change" in i.name:
                    x.append({"Edit": i.id})
                elif "delete" in i.name:
                    x.append({"Delete": i.id})
                
            try:
                l1.append(x)
            except:
                pass

        permission_id = u.user_permissions.filter(user__slug=slug)
        l = []
        for i in permission_id:
            l.append(i.id)
        subadmin = User.objects.get(slug=slug)
        user = User.objects.get(slug=slug)
        return render(request, "admin/subadmin/edit-subadmin.html", {
                       "subadmin": subadmin,
                "user": user,
                "userdata": userdata,
                "l": l1,
                "list": l,
                "job_category":job_category,})

def delete_subadmin(request,slug):
    data = User.objects.get(slug=slug)
    data.delete()
    messages.success(request, "Subadmin user deleted successfully !!!")
    return redirect('/admin/subadmin')

def view_subadmin(request, slug):
    user = User.objects.get(slug=slug)
    return render(request, "admin/subadmin/view-subadmin.html",{'user':user})

def assignJoblist(request,slug):
    user = User.objects.get(slug=slug)
    if user.roll == "Subadmin":
        assign_job = Assign_job.objects.filter(user_id = user.id)
        return render(request, "admin/jobs/assign-job.html",{'assign_job':assign_job})  
    else:
        assign_job = Assign_job.objects.all()
        return render(request, "admin/jobs/assign-job.html",{'assign_job':assign_job})

def ViewassignJob(request):
    if request.method == "POST":
        job_id = request.POST.get("job_id")
        user_id = request.POST.get("user_id")
        if job_id and user_id is not None:
            job = Assign_job.objects.get(job_id = job_id)
            
            return JsonResponse({"status": "success", 'job_title':job.job.job_title,"company_name":job.job.company_name, "subadmin":job.user.username, 'assign_job_status':job.assign_job_status,
                                 "job_slug":job.job.slug,"user_slug":job.user.slug})
        
    # user = User.objects.get()
    
   
    return render(request, "admin/jobs/assign-job.html")


def jobCategory(request):
    job = JobCategory.objects.all()
    return render(request, "admin/jobs/job-category/jobcategory.html",{"job":job})

def add_category(request):
    if request.method=="POST":
        category_name = request.POST.get("category_name")
        if category_name:
            cat = JobCategory.objects.create(name=category_name)
            cat.save()
            messages.success(request, "Job created successfully !!!!")
            return redirect("/admin/job-category/")
        else:
            messages.error(request, "Please fill job name !!!!")
            return redirect("/admin/add-category/")
    return render(request, "admin/jobs/job-category/add_category.html")

def edit_category(request, slug):
    category = JobCategory.objects.get(slug=slug)
    if request.method=="POST":
        category_name = request.POST.get("category_name")
        if category_name:
            category.name = category_name
            category.save()
            messages.success(request, "Job edited successfully !!!!")
            return redirect("/admin/job-category/")
        else:
            messages.error(request, "Please fill job name !!!!")
            return redirect("/admin/edit-category/" + str(slug))
    return render(request, "admin/jobs/job-category/edit_category.html",{'category':category})
 
def delete_category(request, slug):
    job = JobCategory.objects.get(slug=slug)
    job.delete()
    messages.success(request, "Job  deleted successfully !!!")
    return redirect('/admin/job-category')

def assign_job_status(request, id):
    data = Assign_job.objects.get(id=id)
    if request.method == "POST":
        assign_status = request.POST.get("assign_status")
        if assign_status:
            data.assign_job_status = assign_status
            data.save()
            return JsonResponse({"status":"success", "message":"Status change successfully !!!! "})
        return JsonResponse({"status":"error", "message":" data not found !!!! "})
    return JsonResponse({"status":"error", "message":"something went wrong "})


def cmspageList(request):
    cms = Cms_pages.objects.all() 
    return render(request, "admin/cmspage/cms_list.html", {'cms':cms})


def csmPage(request , slug):
    cms_page = Cms_pages.objects.get(slug=slug)
    if request.method == "POST":
        heading1 = request.POST.get('Heading1')
        image1 = request.FILES.get('Image1') 
        heading2 = request.POST.get('Heading2') 
        heading3 = request.POST.get('Heading3') 
        paragraph1 = request.POST.get('Paragraph1') 
        paragraph2 = request.POST.get('Paragraph2') 
        image2 = request.FILES.get('Image2') 
        if heading1 and image1 and heading2 and heading3 and paragraph1 and paragraph2 and image2:
            cms_page.heading1 = heading1
            cms_page.image1 = image1
            cms_page.heading2 = heading2
            cms_page.heading3 = heading3
            cms_page.paragraph1 = paragraph1
            cms_page.paragraph2 = paragraph2
            cms_page.image2 = image2 
            cms_page.save()
            messages.success(request, "Data saved successfully !!!")
            return redirect('/admin/edit-cms-pages/'+ str(slug))
        elif image1:
                cms_page.heading1 = heading1
                cms_page.heading2 = heading2
                cms_page.image1 = image1
                cms_page.heading3 = heading3
                cms_page.paragraph1 = paragraph1
                cms_page.paragraph2 = paragraph2
                cms_page.save()
                messages.success(request, "Data saved successfully !!!")
                return redirect('/admin/edit-cms-pages/'+ str(slug))
        elif image2:
                cms_page.heading1 = heading1
                cms_page.heading2 = heading2
                cms_page.heading3 = heading3
                cms_page.paragraph1 = paragraph1
                cms_page.paragraph2 = paragraph2
                cms_page.image2 = image2 
                cms_page.save()
                messages.success(request, "Data saved successfully !!!")
                return redirect('/admin/edit-cms-pages/'+ str(slug))
        else:
            cms_page.heading1 = heading1
            cms_page.heading2 = heading2
            cms_page.heading3 = heading3
            cms_page.paragraph1 = paragraph1
            cms_page.paragraph2 = paragraph2
            cms_page.save()
            messages.success(request, "Data saved successfully !!!")
            return redirect('/admin/edit-cms-pages/'+ str(slug))   
    return render(request, "admin/cmspage/cms_page.html",{'cms_page':cms_page})


def blogCategory(request):
    data = BlogCategory.objects.all()
    return render(request, "admin/blogs/blog-category/blogcategory.html",{'blogcategory':data})


def add_blogCategory(request):
    if request.method == "POST":
        title = request.POST.get("blog_cat_name")
        if title:
            data = BlogCategory.objects.create(title=title)
            messages.success(request, "blog category create successfully  !!!!!!")
            return redirect('/admin/blogCategory/')
        else:
            messages.error(request, " All fields are required !!!!!!")
            return redirect('/admin/blogCategory/')
            
    return render(request, "admin/blogs/blog-category/add-blog-category.html")

def edit_blogCategory(request,slug):
    data = BlogCategory.objects.get(slug=slug)
    if request.method == "POST":
        title = request.POST.get("blog_cat_name")
        if title:
            data.title = title
            data.save()
            messages.success(request, "blog category update successfully  !!!!!!")
            return redirect('/admin/blogCategory/')
        else:
            messages.error(request, " All fields are required !!!!!!")
            return redirect('/admin/blogCategory/')
    return render(request, "admin/blogs/blog-category/edit-blog-category.html",{'blogcategory':data})

def delete_blogCategory(request, slug):
    blog = BlogCategory.objects.get(slug=slug)
    blog.delete()
    messages.success(request, "blog category deleted successfully !!!")
    return redirect('/admin/blog/')


def blog(request):
    data = Blog.objects.all()
    return render(request, "admin/blogs/blog.html",{'blog':data})


def add_blog(request):
    data = BlogCategory.objects.all()
    if request.method== "POST":
        title = request.POST.get("blog_name")
        image = request.FILES.get("blog_image")
        category = request.POST.get("blog_category")
        description = request.POST.get("blog_description")
        if title and image and category and description:
            data = Blog.objects.create(title=title, image=image, category_id =category, description=description, author=request.user.username)
            messages.success(request , "blog is created successfully !!!!")
            return redirect('/admin/blog/')
        else:
            messages.error(request , "All fields are required !!!!")
            return redirect('/admin/blog/') 
    return render(request, "admin/blogs/add-blog.html",{'data':data})


def edit_blog(request,slug):
    data = BlogCategory.objects.all()
    blog =  Blog.objects.get(slug=slug)
    if request.method== "POST":
        title = request.POST.get("blog_name")
        image = request.FILES.get("blog_image")
        category = request.POST.get("blog_category")
        description = request.POST.get("blog_description")
        if title and image and category and description:
            blog.title=title
            blog.image=image
            blog.category_id =category
            blog.description=description
            blog.save()
            messages.success(request , "blog is created successfully !!!!")
            return redirect('/admin/blog/')
        elif image is None:
                blog.title=title
                blog.category_id =category
                blog.description=description
                blog.save()
                messages.success(request , "blog is created successfully !!!!")
                return redirect('/admin/blog/')
            
        else:
            messages.error(request , "All fields are required !!!!")
            return redirect('/admin/blog/') 
    return render(request, "admin/blogs/edit-blog.html",{'data':data, 'blog':blog})

def delete_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    blog.delete()
    messages.success(request, "blog  deleted successfully !!!")
    return redirect('/admin/blog/')
