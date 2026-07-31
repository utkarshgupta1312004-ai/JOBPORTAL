from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.models import LoginInfo, JobSeeker, Enquiry
from .models import JobInfo
from userapp.models import Response, AppliedJob

import datetime
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admindash(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')

    jobseekers_count = JobSeeker.objects.count()
    jobs_count = JobInfo.objects.count()
    applications_count = AppliedJob.objects.count()
    pending_count = AppliedJob.objects.filter(status='Request Pending').count()
    accepted_count = AppliedJob.objects.filter(status='Accepted').count()
    rejected_count = AppliedJob.objects.filter(status='Rejected').count()
    enquiries_count = Enquiry.objects.count()
    feedback_count = Response.objects.filter(responsetype='Feedback').count()
    complaint_count = Response.objects.filter(responsetype='Complaint').count()
    recent_applicants = AppliedJob.objects.all().order_by('-id')[:5]
    recent_jobs = JobInfo.objects.all().order_by('-id')[:5]

    context = {
        'adminid': adminid,
        'jobseekers_count': jobseekers_count,
        'jobs_count': jobs_count,
        'applications_count': applications_count,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'enquiries_count': enquiries_count,
        'feedback_count': feedback_count,
        'complaint_count': complaint_count,
        'recent_applicants': recent_applicants,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'admindash.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogout(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, "Please Login first!!! ")
        return redirect('login')
    del request.session['adminid']
    messages.success(request, "You have logged-out Successfully")
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    js = JobSeeker.objects.all()
    return render(request, 'jobseekers.html', {"js": js, "adminid": adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def postjob(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')

    if request.method == "POST":
        title = request.POST.get("title")
        skill_required = request.POST.get("skill_required") or request.POST.get("skills_required", "")
        description = request.POST.get("description")
        location = request.POST.get("location")
        salary = request.POST.get("salary")
        jobtype = request.POST.get("jobtype")
        lastdate = request.POST.get("lastdate")
        posteddate = datetime.date.today().strftime("%d/%m/%y")
        ji = JobInfo(
            title=title,
            skill_required=skill_required,
            description=description,
            location=location,
            salary=salary,
            jobtype=jobtype,
            lastdate=lastdate,
            posteddate=posteddate
        )
        ji.save()
        messages.success(request, 'Job Posted Successfully')
        return redirect('postjob')

    return render(request, 'postjob.html', {"adminid": adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def postedjob(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    js = JobInfo.objects.all()
    return render(request, 'postedjob.html', {"js": js, "adminid": adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewenquiries(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    enq = Enquiry.objects.all().order_by('-id')
    return render(request, 'viewenquiries.html', {'enq': enq, 'adminid': adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changeadminpwd(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')

    if request.method == "POST":
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        confirmpassword = request.POST.get("confirmpassword")
        if newpassword != confirmpassword:
            messages.error(request, 'New Password and Confirm Password are not equal')
            return redirect("changeadminpwd")
        try:
            obj = LoginInfo.objects.get(username=adminid, password=oldpassword)
            LoginInfo.objects.filter(username=adminid).update(password=newpassword)
            messages.success(request, 'Password updated Successfully')
            return redirect('adminlogout')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Old password does not match")
            return redirect('changeadminpwd')

    return render(request, 'changeadminpwd.html', {'adminid': adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewfeedback(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    res = Response.objects.filter(responsetype="Feedback")
    return render(request, 'viewfeedback.html', {"res": res, "adminid": adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewcomplaint(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    res = Response.objects.filter(responsetype="Complaint")
    return render(request, 'viewcomplaint.html', {"res": res, "adminid": adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteenq(request, id):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    enq = get_object_or_404(Enquiry, id=id)
    enq.delete()
    messages.success(request, 'Enquiry is deleted Successfully')
    return redirect('viewenquiries')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecom(request, id):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    enq = get_object_or_404(Response, id=id)
    enq.delete()
    messages.success(request, 'Complaint is deleted Successfully')
    return redirect('viewcomplaint')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletefeed(request, id):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    enq = get_object_or_404(Response, id=id)
    enq.delete()
    messages.success(request, 'Feedback is deleted Successfully')
    return redirect('viewfeedback')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletejob(request, id):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    enq = get_object_or_404(JobInfo, id=id)
    enq.delete()
    messages.success(request, 'Job is deleted Successfully')
    return redirect('postedjob')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewapplicant(request):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    applicants = AppliedJob.objects.all().order_by('-id')
    return render(request, 'viewapplicant.html', {'applicants': applicants, 'adminid': adminid})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def acceptapplicant(request, id):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    app = get_object_or_404(AppliedJob, id=id)
    app.status = 'Accepted'
    app.save()
    messages.success(request, 'Applicant Status Updated to Accepted')
    return redirect('viewapplicant')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectapplicant(request, id):
    adminid = request.session.get('adminid')
    if not adminid:
        messages.error(request, 'Please Login first!!! ')
        return redirect('login')
    app = get_object_or_404(AppliedJob, id=id)
    app.status = 'Rejected'
    app.save()
    messages.success(request, 'Applicant Status Updated to Rejected')
    return redirect('viewapplicant')
