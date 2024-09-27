from django.contrib import admin
from profiles.models import ProfileUser, Certificate
# Register your models here.

@admin.register(ProfileUser)
class ProfileCustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'slug', 'created', 'last_updated',)
    search_fields = ('full_name', 'slug')
    prepopulated_fields = {'slug': ('full_name',)}


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('course', 'student',)

