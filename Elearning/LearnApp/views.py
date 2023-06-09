from .permissions import IsTeacher
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer, CourseSerializer, \
    StudentCourseSerializer, UserCreateSerializer, ReviewSerializer
from .models import Student, Teacher, User, Course, StudentCourse, StudentModule, Review
from rest_framework import status, permissions, decorators
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken


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
        filter_fields = (
            'specialization',
            'skill_tags',
        )
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
    "Creating a user , specifying role"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CourseList(APIView):
    "List of courses with filter on tags and title"

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        pagination_class = PageNumberPagination
        filter_fields = (
            'title',
            'tags',
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        permission_classes = [IsTeacher]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudeCourseDetail(APIView):
    "CRUD operations regarding a student-course"

    def get_object(self, pk):
        try:
            return StudentCourse.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response("Does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            studentcourse = self.get_object(pk=pk)
            serializer = StudentCourseSerializer(studentcourse)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "ID: {} does not exist.".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            studentcourse = self.get_object(pk)
            serializer = StudentCourseSerializer(studentcourse, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "ID: {} does not exist".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission_classes = [IsTeacher]
        try:
            studentcourse = self.get_object(pk=pk)
            studentcourse.delete()
            return Response({"Success": "The studentcourse table is deleted."}, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "The studentcourse ID {} does not exist".format(pk)},
                            status=status.HTTP_400_BAD_REQUEST)


class StudentModuleDetail(APIView):
    "CRUD operations regarding a student-module"

    def get_object(self, pk):
        try:
            return StudentModule.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response("Does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            studentmodule = self.get_object(pk=pk)
            serializer = StudentCourseSerializer(studentmodule)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "ID: {} does not exist.".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            studentmodule = self.get_object(pk)

            serializer = StudentCourseSerializer(studentmodule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "ID: {} does not exist".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission_classes = [IsTeacher]
        try:
            studentcourse = self.get_object(pk=pk)
            studentcourse.delete()
            return Response({"Success": "The studentmodule table is deleted."}, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "The studentmodule ID {} does not exist".format(pk)},
                            status=status.HTTP_400_BAD_REQUEST)


class UpdateCompletionStatus(APIView):
    "For updating completion status according to the progress of a course for a student id"

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response("Student does not exist.", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            student = self.get_object(pk)
            courses = student.studentcourses.all()

            for item in courses:

                if item.progress == 100:
                    return Response({"You have successfully completed the course {}".format(item.course.title)},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"Great going; Course {} is in progress".format(item.course.title)},
                                    status=status.HTTP_200_OK)


        except:
            return Response("Student does not exist.", status=status.HTTP_400_BAD_REQUEST)


class ReviewList(APIView):
    def get(self, request):
        teachers = Review.objects.all()
        serializers = ReviewSerializer(teachers, many=True)
        pagination_class = PageNumberPagination
        filter_fields = (
            'student',
            'course',
        )
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    "For registering a user using jwt authentication"
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return Response(res, status.HTTP_201_CREATED)
