# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from  courses.models import Notification, Enrollment, Likes
from instructors.models import Instructor


@receiver(post_save, sender=Likes)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        try:
            # Get the Instructor associated with the course owner
            instructor = Instructor.objects.get(user=instance.course.owner)

            # Create the notification
            Notification.objects.create(
                instructor=instructor,          # Use the Instructor instance
                student=instance.user,          # The user who liked the course
                action='liked',
                course=instance.course
            )
            print("Notification created")
        except Instructor.DoesNotExist:
            print("Instructor not found for the course owner")



@receiver(post_save, sender=Enrollment)
def create_enrollment_notification(sender, instance, created, **kwargs):
    if created:
          # Get the Instructor associated with the course owner
        instructor = Instructor.objects.get(user=instance.course.owner)

        Notification.objects.create(
            instructor=instructor,  # Assuming the owner of the course is the instructor
            student=instance.student.user,
            action='enrolled',
            course=instance.course
        )



