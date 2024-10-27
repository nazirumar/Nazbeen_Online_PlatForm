from datetime import timedelta, timezone
import uuid
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from courses.fields import OrderField
import helpers
from django.core.validators import FileExtensionValidator
import cloudinary.uploader

helpers.cloudinary_init()

def generate_public_id(instance, title=None):
    """Generate a unique public ID for uploaded files."""
    unique_id = str(uuid.uuid4()).replace("-", "")
    if title:
        slug = slugify(title)
        return f"{slug}-{unique_id[:32]}"
    return unique_id

def get_public_id_prefix(instance):
    """Generate public ID prefix based on the instance's class and existing public ID."""
    path = getattr(instance, 'path', None) or ''
    path = path.strip("/")
    public_id = instance.public_id or ''
    model_name = slugify(instance.__class__.__name__)
    return f"{model_name}/{public_id}" if public_id else model_name

def get_display_name(instance):
    """Return the display name for the instance."""
    return getattr(instance, 'get_display_name', lambda: instance.title)()

# Base model for common attributes
class BaseContent(models.Model):
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self, self.title)
        if self.title:
            self.title = self.title.title() 
        super().save(*args, **kwargs)

class Category(BaseContent):
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["created_at"]

    def __str__(self):
        return self.title

class Subject(BaseContent):
    category = models.ForeignKey(Category, related_name="subjects", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey("accounts.customUser", on_delete=models.CASCADE, related_name="subjects_author")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email", "Email required"

class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"

class Course(BaseContent):
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE, related_name="courses_instructure", blank=True, null=True)
    owner = models.ForeignKey("accounts.customUser", on_delete=models.CASCADE, related_name="courses_created", blank=True, null=True)
    subject = models.ForeignKey(Subject, related_name="subject_courses", on_delete=models.CASCADE, null=True, blank=True)
    students = models.ManyToManyField("accounts.customUser", related_name="courses_joined", blank=True)
    description = models.TextField(blank=True, null=True)
    pdf = models.OneToOneField("File", on_delete=models.CASCADE, null=True, blank=True)
    
    image = CloudinaryField(
        "image", 
        null=True, 
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["course", "thumbnail"]
    )
    
    access = models.CharField(max_length=10, choices=AccessRequirement.choices, default=AccessRequirement.EMAIL_REQUIRED, null=True, blank=True)
    status = models.CharField(max_length=10, choices=PublishStatus.choices, default=PublishStatus.DRAFT, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField("accounts.customUser", through="Likes", related_name="liked_courses", blank=True)
    
    total_ratings = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

class CourseMetrics(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='metrics')
    total_views = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_downloads = models.PositiveIntegerField(default=0)
    total_enrollments = models.PositiveIntegerField(default=0)
    total_dislikes = models.PositiveIntegerField(default=0)

class Likes(models.Model):
    user = models.ForeignKey("accounts.customUser", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} likes {self.course.title}"

class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE, blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    order = OrderField(blank=True, for_fields=["course"])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Course: {self.course} -- Module: {self.title}"

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self, self.title)
        super().save(*args, **kwargs)

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=["module"])
    
    thumbnail = CloudinaryField("image", 
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=['thumbnail', 'lesson'],
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Lesson: {self.title} - Module: {self.module.title}'

class LessonVideo(models.Model):
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")
    duration = models.DurationField(blank=True, null=True)
    
    video = CloudinaryField("video", 
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,                
        blank=True, null=True, type='private',
        tags=['video', 'lesson'], resource_type='video'
    )
    
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - Lesson: {self.lesson.title}"

class File(models.Model):
    pdf_file = models.FileField(upload_to="lesson/pdf")

class Student(models.Model):
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    user = models.OneToOneField("accounts.customUser", on_delete=models.CASCADE, related_name="students")
    enrolled_courses = models.ManyToManyField(Course, through="Enrollment")

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self.user.username) 
        super().save(*args, **kwargs)

class EnrollmentStatus(models.TextChoices):
    PENDING = ("pending", "Pending")
    COMPLETED = ("completed", "Completed")
    CANCELLED = ("cancelled", "Cancelled")

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=EnrollmentStatus.choices, default=EnrollmentStatus.PENDING)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    module = models.ForeignKey(Module, related_name="quizzes", on_delete=models.CASCADE, blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
    TRUE_FALSE = "true_false", "True / False"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} - Quiz: {self.quiz.title}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} - Question: {self.question.text}"


class Notification(models.Model):
    INSTRUCTOR_ACTIONS = [
        ('enrolled', 'Student Enrolled'),
        ('feedback', 'Feedback Received'),
        ('liked', 'Course Liked'),
    ]
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE, related_name='instructor_notifications',blank=True, null=True)
    student = models.ForeignKey("accounts.customUser", on_delete=models.CASCADE, related_name='student_notifications', blank=True, null=True, )
    action = models.CharField(max_length=10, choices=INSTRUCTOR_ACTIONS, blank=True, null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} {self.get_action_display()} on {self.course}"