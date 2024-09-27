from django.db import models

from courses.models import generate_public_id

# Create your models here.

class Instructor(models.Model):
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    user = models.OneToOneField("accounts.customUser", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='instructor_profiles/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Instructor"
    
    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        if self.title:
            self.title = self.title.title() 
        super().save(*args, **kwargs)


