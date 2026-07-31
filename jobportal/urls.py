"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views
from adminapp.views import *
from userapp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    #admin urls
    path('admindash/', admindash,name="admindash"),
    path('adminlogout/',adminlogout,name="adminlogout"),
    path('jobseekers/',jobseeker,name='jobseekers'),
    path('postjob/',postjob,name='postjob'),
    path('postedjob/',postedjob,name='postedjob'),
    path('viewenquiries/',viewenquiries,name='viewenquiries'),
    path('changeadminpwd/',changeadminpwd,name='changeadminpwd'),
    path('viewfeedback/',viewfeedback,name='viewfeedback'),
    path('viewcomplaint/',viewcomplaint,name='viewcomplaint'),
    path('deleteenq/<id>',deleteenq,name='deleteenq'),
    path('deletecom/<id>',deletecom,name='deletecom'),
    path('deletefeed/<id>',deletefeed,name='deletefeed'),
    path('deletejob/<id>',deletejob,name='deletejob'),

    path('viewapplicant/',viewapplicant,name='viewapplicant'),
    path('acceptapplicant/<id>',acceptapplicant,name='acceptapplicant'),
    path('rejectapplicant/<id>',rejectapplicant,name='rejectapplicant'),




    #user urls
    path('userdash/',userdash,name='userdash'),
    path('userlogout/',userlogout,name='userlogout'),
    path('userprofile/',userprofile,name='userprofile'),
    path('viewjobs/',viewjobs,name='viewjobs'),
    path('applyjob/<id>',applyjob,name='applyjob'),
    path('changeuserpwd/',changeuserpwd,name='changeuserpwd'),
    path('giveresponse/',giveresponse,name='giveresponse'),

]

