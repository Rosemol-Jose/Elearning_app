import uuid as uuid
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType



# Create your models here.
class Teacher(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    specialization = models.TextField(max_length=100)


class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
        (3, 'admin'),
    )

    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user1 = models.OneToOneField(User,related_name='user', on_delete=models.CASCADE)
    contact = models.IntegerField()
    email = models.EmailField(max_length=50)
    age = models.IntegerField()
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    is_subscribed= models.BooleanField(default=False)


class Student(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    interested_field=models.CharField(max_length=50)


# class Subject(models.Model):
#     language=models.CharField(max_length=30)
class Course(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.TextField(max_length=50)
    duration = models.DurationField(default=1)
    added_by = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    # tags=models.ManyToManyField(Subject)
    # the tags input does contain commas or double quotes then
    # On clicking the particular tag, There will come a list of all the posts associated with that particular tag.
    tags = TaggableManager()


class Module(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    course = models.ForeignKey(Course,related_name='modulecourse', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    mod_num = models.IntegerField( default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['mod_num']

    def __str__(self):
        return f' {self.title}'


class Content(models.Model):
    CHOICES=((1,'text'), (2,'video'), (3,'image'), (4,'file'))
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    module = models.ForeignKey(Module,related_name='module_c' ,on_delete=models.CASCADE)
    content_type = models.PositiveSmallIntegerField(choices=CHOICES)
    # object_id = models.PositiveIntegerField(default=1)
    # item = GenericForeignKey('content_type', 'object_id')
    created_date = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    course=models.ForeignKey(Course,related_name='courses',on_delete=models.CASCADE)
    student=models.ForeignKey(Student,related_name='student_rev',on_delete=models.CASCADE)
    comment=models.TextField(max_length=30)
    # rating = RatingField(range=5)
    rating=models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

class StudentCourse(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    student=models.ForeignKey(Student,related_name='student_c',on_delete=models.CASCADE)
    course=models.ForeignKey(Course,related_name='studentcourse',on_delete=models.CASCADE)
    joining=models.DateTimeField(auto_now_add=True)
    progress=models.IntegerField(blank=True, default=0)


    @property
    def progress_in_percentage(self):
        return f"{self.progress} %"

class StudentModule(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    is_completed=models.BooleanField(default=False)
    student=models.ForeignKey(Student,related_name='student_m',on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='module_s',on_delete=models.CASCADE)


