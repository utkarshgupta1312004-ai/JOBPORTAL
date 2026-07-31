from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from mainapp.models import JobSeeker,LoginInfo
from adminapp.models import JobInfo
from .models import Response, AppliedJob
import datetime
# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userdash(request):
    try:
        if request.session['userid']!=None:
            js = JobSeeker.objects.get(emailaddress=request.session['userid'])
            total_applied = AppliedJob.objects.filter(jobseeker=js).count()
            pending_applied = AppliedJob.objects.filter(jobseeker=js, status='Request Pending').count()
            accepted_applied = AppliedJob.objects.filter(jobseeker=js, status='Accepted').count()
            rejected_applied = AppliedJob.objects.filter(jobseeker=js, status='Rejected').count()
            total_jobs = JobInfo.objects.count()
            my_applications = AppliedJob.objects.filter(jobseeker=js).order_by('-id')[:5]

            context = {
                'js': js,
                'total_applied': total_applied,
                'pending_applied': pending_applied,
                'accepted_applied': accepted_applied,
                'rejected_applied': rejected_applied,
                'total_jobs': total_jobs,
                'my_applications': my_applications,
            }
            return render(request, 'userdash.html', context)
    except KeyError:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userlogout(request):
    try:
        if request.session['userid']!=None:
            del request.session['userid']
            messages.success(request,'Logout Succesfully !!!!')
            return redirect('login')
    except KeyError:
        messages.error(request,'Please Login first !!')
        return redirect('login')

    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def giveresponse(request):
    try:
        if request.session['userid']!=None:
            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            if request.method=="POST":
                responsetype=request.POST.get("responsetype")
                subject=request.POST.get("subject")
                responsetext=request.POST.get("responsetext")
                name=js.name
                contactno=js.contactno
                posteddate=datetime.datetime.today().strftime('%d/%m/%Y')
                res=Response(name=name,contactno=contactno,responsetype=responsetype,responsetext=responsetext,subject=subject,posteddate=posteddate)
                res.save()
                messages.success(request,'Response Sent Successfully')
                return redirect('giveresponse')

            return render(request,'giveresponse.html',{'js':js})
    except KeyError:
        messages.error(request,'Pease Login first!!! ')
        return redirect('login')





    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userprofile(request):
    try:
        if request.session['userid']!=None:
            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            return render(request,'userprofile.html',{'js':js})
    except KeyError:
        messages.error(request,'Pease Login first!!! ')
        return redirect('login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewjobs(request):
    try:
        if request.session['userid']!=None:
            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            ji=JobInfo.objects.all()
            applied_qs=AppliedJob.objects.filter(jobseeker=js)
            has_applied = applied_qs.exists()
            applied_dict={app.job_id: app.status for app in applied_qs}
            for j in ji:
                j.applied_status = applied_dict.get(j.id, None)
            return render(request,'viewjobs.html',{'js':js,'ji':ji,'has_applied':has_applied})
    except KeyError:
        messages.error(request,'Please Login first!!! ')
        return redirect('login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def applyjob(request, id):
    try:
        if request.session['userid']!=None:
            js = JobSeeker.objects.get(emailaddress=request.session['userid'])
            job = JobInfo.objects.get(id=id)
            today = datetime.datetime.today().strftime('%d/%m/%Y')
            
            if AppliedJob.objects.filter(jobseeker=js).exists():
                if AppliedJob.objects.filter(job=job, jobseeker=js).exists():
                    messages.info(request, 'You have already applied for this job.')
                else:
                    messages.warning(request, 'You are allowed to apply for only one job at a time!')
            else:
                AppliedJob.objects.create(
                    job=job,
                    jobseeker=js,
                    applieddate=today,
                    status='Request Pending'
                )
                messages.success(request, 'Applied successfully!')
            return redirect('viewjobs')
    except KeyError:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def changeuserpwd(request):
    try:
        if request.session['userid']!=None:
            if request.method=="POST":
                oldpassword=request.POST.get("oldpassword")
                newpassword=request.POST.get("newpassword")
                confirmpassword=request.POST.get("confirmpassword")
                if newpassword!=confirmpassword:
                    messages.error(request,'New Password and  Confirm Password are not equal')
                    return redirect("changeuserpwd")
                elif oldpassword==newpassword:
                    messages.error(request,'Old password and new password are not equal')
                    return redirect('changeuserpwd')
                try:
                    obj=LoginInfo.objects.get(username=request.session['userid'],password=oldpassword)
                    LoginInfo.objects.filter(username=request.session['userid']).update(password=newpassword)
                    
                    messages.success(request,'Password updated Successfully')
                    return redirect('userlogout')
                except:
                    messages.error(request,"Old password is not match")
                    return redirect('changeuserpwd')
        return render(request,'changeuserpwd.html')
    except KeyError:
        messages.error(request,'Please Login first!!! ')
        return redirect('login') 