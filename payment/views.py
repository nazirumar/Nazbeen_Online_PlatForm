# views.py

import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from courses.models import Enrollment
from .models import Course, Payment, Student
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student, _ = Student.objects.get_or_create(user=request.user)

    # Create Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'NGN',
                'product_data': {
                    'name': course.title,
                },
                'unit_amount': int(course.price * Decimal(100)),  # Stripe expects amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment_success', args=[course.id])
        ),
        cancel_url=request.build_absolute_uri(reverse('course_detail', args=[course.id])),
    )

    return JsonResponse({'sessionId': checkout_session.id})

@login_required
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student, _ = Student.objects.get_or_create(user=request.user)

    # Check if the student is already enrolled
    if not Enrollment.objects.filter(student=student, course=course).exists():
        # Create enrollment and payment records
        enrollment = Enrollment.objects.create(
            student=student, 
            course=course, 
            enrolled_at=timezone.now()
        )

        Payment.objects.create(
            student=student,
            course=course,
            amount=course.price,
            payment_date=timezone.now(),
            payment_status='Completed'
        )

    return render(request, 'payment_success.html', {'course': course})
