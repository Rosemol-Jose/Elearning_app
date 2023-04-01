import views as views
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import registration

urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='courses'),
    path('students/', views.StudentList.as_view(), name='student_list'),
    path('students/<str:pk>', views.StudentDetail.as_view(), name='student_details'),
    path('teachers/', views.TeacherList.as_view(), name='teacher_list'),
    path('teachers/<str:pk>', views.TeacherDetail.as_view(), name='teacher-details'),
    path('studentcourse/<str:pk>', views.StudeCourseDetail.as_view(), name='studentcourse'),
    path('studentmodule/<str:pk>', views.StudentModuleDetailas_view(), name='studentmodule'),
    path('progress/<str:pk>', views.UpdateCourse.as_view(), name='progress'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', registration, name='register'),


]



