import views as views
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('courses', views.CourseList.as_view(), name='course_detail'),

]



