from django.contrib import admin

from instructors.models import Certificate, Instructor

# Register your models here.

admin.site.register(Instructor)



@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('course', 'student',)

