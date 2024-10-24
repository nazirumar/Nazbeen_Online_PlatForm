from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Enrollment, EnrollmentStatus
from instructors.models import Certificate
from .models import ProfileUser, generate_certificate_pdf

User = get_user_model()


@receiver(post_save, sender=User)
def create_staff_for_new_user(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)



@receiver(post_save, sender=Enrollment)
def create_certificate(sender, instance, **kwargs):
    # Assuming Enrollment has a `status` field that marks completion
    if instance.status == EnrollmentStatus.COMPLETED:
        # Check if a certificate already exists for this student and course
        certificate, created = Certificate.objects.get_or_create(
            student=instance.student,
            course=instance.course
        )
        if created:
            # Generate the certificate PDF
            pdf_generated = generate_certificate_pdf(certificate)
            if pdf_generated:
                print(f"Certificate generated for {certificate.student.user.username}")
            else:
                print(f"Failed to generate certificate for {certificate.student.user.username}")


