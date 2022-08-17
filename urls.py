"""ITFest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from FestApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('studentreg', views.studentreg, name='studentreg'),
    path('login', views.login, name='login'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('studenthome', views.studenthome, name='studenthome'),
    path('approvestudents', views.approvestudents, name='approvestudents'),
    path('acceptstudent', views.acceptstudent, name='acceptstudent'),
    path('addcoordinator', views.addcoordinator, name='addcoordinator'),
    path('addjudge', views.addjudge, name='addjudge'),
    path('coordinatorhome', views.coordinatorhome, name='coordinatorhome'),
    path('addevent', views.addevent, name='addevent'),
    path('viewevents', views.viewevents, name='viewevents'),
    path('participate', views.participate, name='participate'),
    path('allocatejudge', views.allocatejudge, name='allocatejudge'),
    path('selectevent', views.selectevent, name='selectevent'),
    path('selectjudge', views.selectjudge, name='selectjudge'),
    path('judgehome', views.judgehome, name='judgehome'),
    path('viewallocation', views.viewallocation, name='viewallocation'),
    path('plist', views.plist, name='plist'),
    path('viewparticipants', views.viewparticipants, name='viewparticipants'),
    path('addfeedback', views.addfeedback, name='addfeedback'),
    path('viewfeedback', views.viewfeedback, name='viewfeedback'),
    path('viewwinner', views.viewwinner, name='viewwinner'),
    path('viewmarks', views.viewmarks, name='viewmarks'),
    path('viewwinnerstudent', views.viewwinnerstudent, name='viewwinnerstudent'),
    path('addmarks', views.addmarks, name='addmarks'),
    path('addwinner', views.addwinner, name='addwinner'),
    path('addmarksjudge', views.addmarksjudge, name='addmarksjudge'),
    path('winner', views.winner, name='winner'),
    path('participateevent', views.participateevent, name='participateevent'),
    path('judviewwinnersstud', views.judviewwinnerstudent,
         name='judviewwinnersstud'),
    path('collegereg', views.collegereg, name='collegereg'),
    path('companyreg', views.companyreg, name='companyreg'),
    path('collegehome', views.collegehome, name='collegehome'),
    path('companyhome', views.companyhome, name='companyhome'),
    path('colviewwinners', views.colviewwinners, name='colviewwinners'),
    path('comviewwinners', views.comviewwinners, name='comviewwinners'),
    path('recruit', views.recruit, name='recruit'),
    path('comViewRecruit', views.comViewRecruit, name='comViewRecruit'),
    path('studentviewrecruit', views.studentviewrecruit, name='studentviewrecruit'),







]
