from django.db import models
from django.conf import settings
from django.utils.text import slugify

from courses.models import Course, Enrollment, Student

# Create your models here.


class ProfileUser(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio  = models.TextField(max_length=2000, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile/img', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    courses_enrollments = models.ManyToManyField(Enrollment, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

        
        
    def __str__(self):
        return str(self.full_name)




class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f'{self.student.user.username} - {self.course.title} Certificate'

