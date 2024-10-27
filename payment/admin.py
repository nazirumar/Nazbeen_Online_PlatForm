from django.contrib import admin

# Register your models here.


from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'payment_date', 'payment_status', 'stripe_payment_id', 'transaction_id')