from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer, CourseSerializer, ContentSerializer
from .models import Student, Teacher, User, Course
from rest_framework.authentication import BasicAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
# Create your views here.
class StudentList(APIView):
    """
    List all students, or create a new student
    """

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        pagination_class = PageNumberPagination
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    """
    Retrieve, update or delete a student
    """

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response("Student does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherList(APIView):
    """
    List all teachers, or create a new teacher.
    """

    def get(self, request):
        teachers = Teacher.objects.all()
        serializers = TeacherSerializer(teachers, many=True)
        pagination_class = PageNumberPagination
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetail(APIView):
    """
    Retrieve, update or delete a teacher.
    """

    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response("Student does not exist.", status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk):
        try:
            teacher = self.get_object(pk=pk)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "TeacherID: {} does not exist.".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            teacher = self.get_object(pk)
            serializer = TeacherSerializer(teacher, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "TeacherID: {} does not exist".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            teacher = self.get_object(pk=pk)
            teacher.delete()
            return Response({"Success": "Teacher is deleted."}, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "TeacherID: {} does not exist".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerializer
    # if is_teacher
    # permission_classes=[IsOwnerOnly]
class CourseList(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        pagination_class = PageNumberPagination
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def is_completed(self):
    #     pass
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)

        # if User.role == 'Student':
        #     course.studentcourses.add(request.user)
        #     return Response({'enrolled': True})






