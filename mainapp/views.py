from django.shortcuts import render,redirect
from .models import LoginInfo
from django.contrib import messages
from .models import JobSeeker,Enquiry
from adminapp.models import  JobInfo
import datetime

# Create your views here.
def index(request):
   
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        contactno=request.POST.get("contactno")
        emailaddress=request.POST.get("emailaddress")
        enquirytext=request.POST.get("enquirytext")
        posteddate=datetime.datetime.today().strftime("%d/%m/%Y")
        enq=Enquiry(name=name,contactno=contactno,emailaddress=emailaddress,enquirytext=enquirytext,posteddate=posteddate)
        enq.save()
        messages.success(request,'Message Sent Succesfully , Our contact team contact you soon ....')
        return redirect('contact')
    return render(request,'contact.html')
def register(request):
    try:
        if request.method=="POST":
                name=request.POST.get("name")
                gender=request.POST.get("gender")
                contactno=request.POST.get("contactno")
                emailaddress=request.POST.get("emailaddress")
                qualification=request.POST.get("qualification")
                experience=request.POST.get("experience")
                keyskill=request.POST.get("keyskill")
                address=request.POST.get("address")
                password=request.POST.get("password")
                js=JobSeeker(name=name,gender=gender,contactno=contactno,emailaddress=emailaddress,qualificaion=qualification,experience=experience,keyskill=keyskill,address=address)
                li=LoginInfo(usertype='jobseeker',username=emailaddress,password=password)
                js.save()
                li.save()
                messages.success(request,"Registration is done")
                return redirect('register')
    except:
        messages.error(request,"This Email has been already registered")
        return redirect("register")
    return render(request,'register.html')

def login(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = LoginInfo.objects.get(username=username,password=password)
            
            if user is not None:
                if user.usertype=='admin':
                   # messages.success(request,"Welcome Admin")
                    request.session['adminid']=user.username
                    return redirect("admindash")
                elif user.usertype=='jobseeker':
                   # messages.success(request,"Welcome Job seeker")
                    request.session['userid']=user.username
                    return redirect("userdash")
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid User and password")
            return redirect("login")
   
    return render(request,'login.html')