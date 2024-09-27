from django.db.models import Q
from django.shortcuts import get_object_or_404
from courses.models import Course, Enrollment, Lesson, Module, PublishStatus, LessonVideo, Student
import logging
from django.db.models import Count

# Initialize a logger for capturing errors
logger = logging.getLogger(__name__)


def get_publish_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)


def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.annotate(
                total_module=Count('modules')
                ).get(status=PublishStatus.PUBLISHED, public_id=course_id)
        print(obj)
    except:
        pass
    return obj


def get_course_lesson_videos(modules=None):
    if not modules:
        return [], None

    try:
        all_videos = []
        last_lesson_public_id = None

        # Iterate through each module and fetch lessons and their videos
        for module in modules:
            lessons = module.lessons.all()
            for lesson in lessons:
                last_lesson_public_id = lesson.public_id
                lesson_videos = lesson.videos.all()
                all_videos.extend(lesson_videos)

        return all_videos, last_lesson_public_id

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error fetching lesson videos: {e}")
        return [], None


def get_lessons_video_watch(course_public_id=None):
    if not course_public_id:
        return None
    try:
            # Retrieve the course using public_id or return a 404 if not found
        course = get_object_or_404(Course, public_id=course_public_id)

        # Retrieve the modules related to the course
        modules = Module.objects.filter(course=course).select_related('course')

        # Retrieve the lessons for the course's modules
        lessons = Lesson.objects.filter(module__course=course).select_related('module')
        videos = LessonVideo.objects.filter(lesson__in=lessons)
        return course, modules, lessons, videos
    except LessonVideo.DoesNotExist:
        return None  # Handle case where no lesson videos are found
    except Exception as e:
        # Log the error in production environment instead of printing
        print(f"Error fetching lessons: {e}")
        return None


def course_enrollment(course_id=None, user=None):
    course = get_object_or_404(Course, public_id=course_id)
    # Get or create the Student instance associated with the logged-in user
    student, created = Student.objects.get_or_create(user=user)
    # Check if the student is already enrolled
    enrollment_exists = Enrollment.objects.filter(student=student, course=course).exists()
    if enrollment_exists:
        message = "You are already enrolled in this course."
    else:
        Enrollment.objects.create(student=student, course=course)
        message = "You have successfully enrolled in the course."
    
    return course, message