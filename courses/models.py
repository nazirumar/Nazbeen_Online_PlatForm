import uuid
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from courses.fields import OrderField
import helpers
from django.core.validators import FileExtensionValidator
import cloudinary.uploader


helpers.cloudinary_init()


def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:32]
    return f"{slug}-{unique_id_short}"

def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{public_id}"

def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload"


# Create your models here.



class BaseContent(models.Model):
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)


    class Meta:
        abstract = True

class Category(BaseContent):
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["created_at"]  # Orders categories alphabetically by name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        if self.title:
            self.title = self.title.title() 
        super().save(*args, **kwargs)


class Subject(BaseContent):
    category = models.ForeignKey(
        Category,
        related_name="subjects",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        "accounts.customUser", on_delete=models.CASCADE, related_name="subjects_author")

    class Meta:
        ordering = ["-created_at"]  # Alphabetical ordering of subjects

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        if self.title:
            self.title = self.title.title() 
        super().save(*args, **kwargs)


class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email", "Email required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


class Course(BaseContent):
    owner = models.ForeignKey(
        "accounts.customUser",  on_delete=models.CASCADE, related_name="courses_created", blank=True
    )
    subject = models.ForeignKey(
        Subject,
        related_name="subject_courses",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    students = models.ManyToManyField(
        "accounts.customUser", related_name="courses_joined", blank=True
    )
    description = models.TextField(
        blank=True, null=True
    )  # Rich text editor field for description
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.OneToOneField("File", on_delete=models.CASCADE, null=True, blank=True)
 # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField(
        "image", 
        null=True, 
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["course", "thumbnail"]
    )
    access = models.CharField(
        max_length=10,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED,
    )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT
    )
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(
        "accounts.customUser", through="Likes", related_name="liked_courses"
    )

    total_ratings = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # Newest courses appear first

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        if self.title:
            self.title = self.title.title() 
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path
    
    @property
    def path(self):
        return f"/elearning/courses/{self.public_id}"

    def get_display_name(self):
        return f"{self.title} - Course"

    def get_thumbnail(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(
            self, 
            field_name='image',
            as_html=False,
            width=382
        )

    def get_display_image(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(
            self, 
            field_name='image',
            as_html=False,
            width=750
        )

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
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} likes {self.course.title}"


class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name="modules", on_delete=models.CASCADE, blank=True, null=True
    )
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=200)
    order = OrderField(blank=True, for_fields=["course"])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]  # Modules are ordered by their order field

    def __str__(self):
        return f"Course: {self.course}. -- Module: {self.title}"

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        if self.title:
            self.title = self.title.title() 
        super().save(*args, **kwargs)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)

    description = models.TextField(
        blank=True, null=True
    )  # Rich text editor field for description
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=["module"])
    thumbnail = CloudinaryField("image", 
                public_id_prefix=get_public_id_prefix,
                display_name=get_display_name,
                tags = ['thumbnail', 'lesson'],
                blank=True, null=True)
    


    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)


    def get_thumbnail(self):
        """Retrieve the thumbnail image or fallback to the lesson video thumbnail."""
        width = 382
        if self.thumbnail:
            return helpers.get_cloudinary_image_object(
                self, 
                field_name='thumbnail',
                format='jpg',
                as_html=False,
                width=width
            )
        # Check if there are videos related to this lesson
        if self.videos.exists():
            # If a video exists, return its thumbnail
            video = self.videos.first()
            if video.video:
                return helpers.get_cloudinary_image_object(
                    video,  # Changed to video for context
                    field_name='video',
                    format='jpg',
                    as_html=False,
                    width=width
                )
        return None

    def get_absolute_url(self):
        return self.path


    def __str__(self):
        return f'Lesson: {self.title} -Module: {self.module}'
    
    @property
    def path(self):
        course_path = self.courses.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"elearning/{course_path}/lessons/{self.public_id}"
    
    def get_latest_video(self):
        video = self.video.lates()
        return video


class LessonVideo(models.Model):
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")
    duration = models.DurationField(blank=True, null=True)
    video = CloudinaryField("video", 
            public_id_prefix=get_public_id_prefix,
            display_name=get_display_name,                
            blank=True, 
            null=True, 
            type='private',
            tags = ['video', 'lesson'],
            resource_type='video')
    url = models.URLField(blank=True, null=True,)

    def __str__(self):
        return self.lesson.title


    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self)
        if self.title:
            self.title = self.title.title() 
        super().save(*args, **kwargs)
   
        
    def get_absolute_url(self):
        return self.path
    
  

 


class File(models.Model):
    pdf_file = models.FileField(upload_to="lesson/pdf")


class Student(models.Model):
    user = models.OneToOneField(
        "accounts.customUser", on_delete=models.CASCADE, related_name="students"
    )
    enrolled_courses = models.ManyToManyField(Course, through="Enrollment")

    def __str__(self):
        return self.user.username


# Enrollment model to track which students are enrolled in which courses
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment')
    progress = models.PositiveIntegerField(
        default=0
    )  # As a percentage of course completion
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"


class Result(models.Model):
    student = models.ForeignKey(
        "accounts.customUser", on_delete=models.CASCADE, related_name="results"
    )
    lesson = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lesson_result"
    )
    score = models.PositiveIntegerField(default=0)
    grade = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.student} - {self.grade}"


class Quiz(models.Model):
    course = models.ForeignKey(
        Course, related_name="quizzes", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    total_marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_text = models.TextField()
    marks = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quiz.title} - Question"


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"


class Review(models.Model):
    course = models.ForeignKey(Course, related_name="reviews", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )  # 1 to 5 stars
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"
