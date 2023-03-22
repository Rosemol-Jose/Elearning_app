import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType





class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
        (3, 'admin'),
    )

    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=12)
    age = models.IntegerField()
    date_of_birth = models.DateField(null=True)
    place = models.CharField(max_length=50)
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    is_subscribed = models.BooleanField(default=False)


class Teacher(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    specialization = models.TextField(max_length=100)
    user = models.ForeignKey(User, related_name='app_teachers', on_delete=models.CASCADE)
    skill_tags = TaggableManager()


class Student(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    interested_field = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='app_students', on_delete=models.CASCADE)


class Course(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.TextField(max_length=50)
    duration = models.DurationField(default=1)
    added_by = models.ForeignKey(Teacher, related_name='app_courses',on_delete=models.CASCADE)
    # On clicking the particular tag, There will come a list of all the posts associated with that particular tag.
    tags = TaggableManager()


class Module(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    course = models.ForeignKey(Course, related_name='app_modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    module_num = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['module_num']

    def __str__(self):
        return f' {self.title}'


class Content(models.Model):
    CHOICES = ((1, 'text'), (2, 'video'), (3, 'image'), (4, 'file'))
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    module = models.ForeignKey(Module, related_name='app_contents', on_delete=models.CASCADE)
    content_type = models.PositiveSmallIntegerField(choices=CHOICES)
    item=models.URLField(max_length = 200)
    created_date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    course = models.ForeignKey(Course, related_name='course_reviews', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='student_reviews', on_delete=models.CASCADE)
    comment = models.TextField(max_length=30)
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)


class StudentCourse(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    student = models.ForeignKey(Student, related_name='studentcourses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)
    joining = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(blank=True, default=0)

    @property
    def progress_in_percentage(self):
        return f"{self.progress} %"


class StudentModule(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_completed = models.BooleanField(default=False)
    student = models.ForeignKey(Student, related_name='studentmodules', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='modules', on_delete=models.CASCADE)
