from django.db import models
from django.conf import settings
from django.utils.text import slugify
from io import BytesIO
from django.template.loader import get_template
from django.core.files import File
from xhtml2pdf import pisa

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




def generate_certificate_pdf(certificate):
    """
    Generates and saves a PDF certificate for a given Certificate instance.
    """
    template_path = 'profile/certificate_template.html'
    context = {
        'certificate': certificate,
        'student': certificate.student,
        'course': certificate.course,
    }

    # Render the HTML template
    template = get_template(template_path)
    html = template.render(context)

    # Create a BytesIO buffer to save the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF and save it to the buffer
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    # If the PDF was generated successfully, save it to the certificate model
    if not pisa_status.err:
        pdf_buffer.seek(0)
        certificate.certificate_file.save(f"certificate_{certificate.student.user.username}.pdf", File(pdf_buffer))
        pdf_buffer.close()

        return True  # PDF generated and saved successfully
    else:
        return False  # Failed to generate PDF

