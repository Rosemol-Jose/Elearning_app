from rest_framework import serializers

from LearnApp.models import User, Content, Module, Student, Teacher, Course, StudentModule, StudentCourse, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
        "input_type": "Password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user



class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ('module', 'item',)

class ModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ('course', 'title', 'description', 'module_num','created_date','contents',)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields ='__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'
class StudentModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentModule
        fields = '__all__'
class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentCourse
        fields='__all__'
class  ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'

