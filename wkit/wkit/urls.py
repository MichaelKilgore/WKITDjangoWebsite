"""wkit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from wkit.admin import site

from django_otp.admin import OTPAdminSite

from . import views

#admin.site = site
#admin.autodiscover()

def _admin_template():
	return 'admin/login.html'

class OTPAdmin(OTPAdminSite):


	def __init__(self, name='otpadmin'):
		super().__init__(name)
		self.login_template = _admin_template()

from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)
#admin_site.autodiscover()

urlpatterns = [
	path('', views.index, name='index'),
	path('home/', views.index, name='home'),
	path('mentor/create/', views.createMentor, name='mentor/create'),
	path('mentor/search/', views.searchMentor, name='mentor/search'),
	path('mentor/profile/<str:id>/', views.mentorProfile, name='mentor/profile'),
	path('program/create/', views.createProgram, name='program/create'),
	path('program/search/', views.searchProgram, name='program/search'),
	path('program/profile/<str:id>/', views.programProfile, name='program/profile'),
	path('student/create/', views.createStudent, name='student/create'),
	path('student/search/', views.searchStudent, name='student/search'),
	path('student/update/', views.updateStudent, name='student/update'),
	path('student/profile/<str:id>/', views.studentProfile, name='student/profile'),
	path('organization/create/', views.createOrganization, name='organization/create'),
	path('organization/search/', views.searchOrganization, name='organization/search'),
	path('organization/profile/<str:id>/', views.organizationProfile, name='organization/profile'),
	path('interest/create/', views.createInterest, name='interest/create'),
	path('interest/search/', views.searchInterest, name='interest/search'),
	path('interest/delete/', views.deleteInterest, name='interest/delete'),
	path('scholarship/create/', views.createScholarship, name='scholarship/create'),
	path('scholarship/search/', views.searchScholarship, name='scholarship/search'),
	path('graph/view/', views.viewGraph, name='graph/view'),
	path('graph/download/', views.downloadGraph, name='graph/download'),
	path('logout/', views.logout, name='logout'),
	path('admin/', admin.site.urls),
]












