from django.db import models
from django.conf import settings

from courses.models import Course, Student, generate_public_id

# Create your models here.

class Instructor(models.Model):
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='instructor_profiles/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Instructor"
    
    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self.user.username)
        super().save(*args, **kwargs)



class Certificate(models.Model):
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, )
    date_awarded = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f'{self.student.user.username} - {self.course.title} Certificate'
    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self.student.user.username)
        super().save(*args, **kwargs)
