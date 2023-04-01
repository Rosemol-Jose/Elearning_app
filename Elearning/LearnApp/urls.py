from rest_framework import permissions
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from .views import registration, ReviewList

schema_view = get_schema_view(
   openapi.Info(
      title="Elearning Docs",
      default_version='v1',
      description="description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@elaerning.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='courses'),
    path('students/', views.StudentList.as_view(), name='student_list'),
    path('students/<str:pk>', views.StudentDetail.as_view(), name='student_details'),
    path('teachers/', views.TeacherList.as_view(), name='teacher_list'),
    path('teachers/<str:pk>', views.TeacherDetail.as_view(), name='teacher-details'),
    path('studentcourse/<str:pk>', views.StudeCourseDetail.as_view(), name='studentcourse'),
    path('studentmodule/<str:pk>', views.StudentModuleDetail.as_view(), name='studentmodule'),
    path('progress/<str:pk>', views.UpdateCompletionStatus.as_view(), name='progress'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', registration, name='register'),
    path('reviews/',  ReviewList.as_view(), name='review'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]




