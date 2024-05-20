"""
URL configuration for scholarhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from scholarhub.views import *
from rest_framework.routers import DefaultRouter
router=DefaultRouter()

router.register('application_viewset',Admin_stud_ApplicationView,basename="admin")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',AdminRegistrationview.as_view(),name="reg"),
    path('st_reg/',StudentRegistrationView.as_view(),name="stu_reg"),
    path('login/',LoginAPI.as_view(),name='login'),
    path('AddScholarship/',AddScholarshipView.as_view(),name="adscholar"),
    path('applyscholarship/',StudentApply.as_view(),name="apply4scholarship"),
    path('list_scholarshipbyadmin/',ListScholarshipforadmin.as_view(),name="4adminlist"),
    path('list_scholarship/',ListScholarshipforStudents.as_view(),name="listscholar"),
    path('list_scholarship/<int:pk>',RetrieveScholarship.as_view(),name='retrieve'),
    # path('list_applied/',ViewAppliedStudents.as_view(),name="listofappliedstudents"),
    # path('list_applied_each/<int:pk>',ViewEachApplied.as_view(),name="list_each"),
    path('list_applied_for_student/<int:pk>',ViewAppliedScholarship.as_view(),name="list_each"),
]+router.urls
