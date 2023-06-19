from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
import uuid
from .manager import CustomUserManager

# Create your models here.

# class Dashboard(models.Model):
#     class Meta:
#         default_permissions = ()
#         permissions = (
#             ("sidebar_dashboard", "Can Sidebar dashboard"),
#             ("view_dashboard", "Can view dashboard"),
#         )

class JobCategory(models.Model):
    name = models.CharField(max_length=100, null=False)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = (
            ("sidebar_jobcategory", "Can sidebar jobcategory"),) 
        

        
class User(AbstractUser):
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE,related_name="jobcat" , null=True, blank=True)
    
    USER_TYPE = (
        ("subadmin", "Subadmin"),
        ("admin", "Admin"),
        ("company", "Company"),
    )
    roll = models.CharField(
        max_length=10,
        choices=USER_TYPE,
    )
    USER_STATUS = (
        ("0", "PENDING"),
        ("1", "APPROVED"),
        ("2", "REJECTED"),
    )
    email = models.EmailField(unique=True)
    Otp = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_gst = models.CharField(max_length=100, null=True, blank=True)
    adhaar_card = models.CharField(
        max_length=50,
    )
    pan_card = models.CharField(
        max_length=50,
    )
    username = models.CharField(max_length=50)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    image = models.ImageField(null=True, blank=True, upload_to="media/img")
    # gender = models.CharField(max_length=50, null=True, blank=True)
    company_mobile_number = models.CharField(
        max_length=50,
    )
    
    company_address = models.CharField(max_length=100, null=True, blank=True)
    user_status = models.CharField(max_length=2, choices=USER_STATUS, default=0)
    work_status = models.CharField(max_length=20,  null=True, blank=True)
    home_address = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    resume = models.FileField(upload_to="resume")
    FillEmpstatus = models.BooleanField(default=False)
    office_address = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    login_source=models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=500, null=True, blank=True)
    # auth_token = models.CharField(max_length=50, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    soft_del_status = models.BooleanField(default=False)
    phone_no_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
  

    def __str__(self):
        return self.email
    
    def soft_delete(self):
        self.soft_del_status = True
        self.save()
    
    class Meta:
        permissions = (
            ("sidebar_user", "Can sidebar user"),)



class JobCategoryCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobcategorycompany")
    
    name = models.CharField(max_length=100, null=False)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = (
            ("sidebar_jobcategory", "Can sidebar jobcategory"),) 

class JobCategoryOptionCompany(models.Model):
    job_category = models.ForeignKey(JobCategoryCompany, on_delete=models.CASCADE, related_name="jobcategorycompanyoption")
    
    name = models.CharField(max_length=100, null=False)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = (
            ("sidebar_jobcategoryoption", "Can sidebar jobcategoryoption"),) 






 
class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="jobpost")
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE,related_name="jobcategory" , null=True, blank=True)
    
    work_place = models.CharField(
        max_length=30,
        
    )
    job_types = models.CharField(
        max_length=30,
        
    )
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    job_title = models.CharField(max_length=50)
    minimum_exp = models.IntegerField()
    maximum_exp = models.IntegerField()
    minimum_annual_salary = models.CharField(max_length=20)
    maximum_annual_salary = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    no_of_emplyoee = models.CharField(max_length=50)
    higher_education = models.CharField(max_length=50)
    job_location = models.CharField(max_length=100)
    job_description= models.CharField(max_length=100)
    skills= models.CharField(max_length=100)
    emp_gender = models.CharField(max_length=100)
    notice_period = models.CharField(max_length=100)
    job_opportunity = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    age_criteria = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    job_status = models.CharField(max_length=50)

    
    class Meta:
        permissions = (
            ("sidebar_jobpost", "Can sidebar jobpost"),)

class Dashboard(models.Model):
    class Meta:
        default_permissions = ()
        permissions = (
            ("sidebar_dashboard", "Can sidebar dashboard"),
            ("view_dashboard", "Can view dashboard"),
        )

class Subadmin(models.Model):
    class Meta:
        default_permissions = ()
        permissions = (
            ("sidebar_subadmin", "Can sidebar subadmin"),
            ("add_subadmin", "can add subadmin"),
            ("change_subadmin", "can change change"),
            ("delete_subadmin", "can delete subadmin"),
            ("view_subadmin", "can view subadmin"),
        )

class Assign_job(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user_id")
    job = models.ForeignKey(JobPost , on_delete=models.CASCADE , related_name="job_id")
    assign_job_status = models.CharField(max_length=200, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = (
            ("sidebar_assign_job", "Can sidebar assign job"),
            
        )
      
class userEmployementDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="UserEmployement")
    current_emp = models.CharField(null=False, blank=False, max_length=30)
    work_exp_year = models.CharField(null=False, blank=False, max_length=30)
    work_exp_month = models.CharField(null=False, blank=False, max_length=30)
    current_company_name = models.CharField(null=True, blank=True, max_length=50)
    pervious_company_name = models.CharField(null=True, blank=True, max_length=50)
    designation  = models.CharField(null=False, blank=False, max_length=50)
    key_skills  = models.TextField(null=False, blank=False)
    it_skills  = models.TextField(null=False, blank=False)
    
    work_type  = models.CharField(null=False, blank=False,max_length=40)
    joining_date  = models.DateField(null=True, blank=True )
    leaving_date  = models.DateField(null=True, blank=True)
    current_salary  = models.CharField(null=True, blank=True,max_length=40)
    notice_period  = models.CharField(null=True, blank=True,max_length=100)
    skills_used = models.CharField(null=True, blank=True,max_length=100)
    
class ApplyJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="Userapply")
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE,related_name="jobapply")
    created_at = models.DateTimeField(auto_now_add=True)
    
class Contact(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField() 
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Cms_pages(models.Model):
    heading1 = models.CharField(max_length=300,null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True)
    heading2 = models.CharField(max_length=300,null=True, blank=True)
    heading3 = models.CharField(max_length=300,null=True, blank=True)
    paragraph1 = models.CharField(max_length=300,null=True, blank=True)
    paragraph2 = models.CharField(max_length=300,null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    slug = models.CharField(null=True, blank=True, max_length=20)
    class Meta:
        permissions = (
            ("sidebar_cms_pages", "Can sidebar cms_pages"),)
        
class BlogCategory(models.Model):
    title = models.CharField(max_length=300,null=True, blank=True)
    slug = models.CharField(null=True, blank=True, unique=True, default=uuid.uuid4,max_length=50)
    created_at = models.DateField(auto_now_add=True)
    
class Blog(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE,related_name="blogCategory")
    title = models.CharField(max_length=300,null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.CharField(null=True, blank=True, unique=True, default=uuid.uuid4,max_length=50)
    description = models.CharField(null=True, blank=True, max_length=500)
    author = models.CharField(null=True, blank=True, max_length=50)
    created_at = models.DateField(auto_now_add=True)
    class Meta:
        permissions = (
            ("sidebar_blog", "Can sidebar blog"),)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



    

