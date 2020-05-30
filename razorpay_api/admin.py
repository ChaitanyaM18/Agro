from django.contrib import admin
from . import models

# Register your models here.


class RazorpayTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'currency_type', 'transaction_id',
                    'status', 'razorpay_id', 'error_code', 'error_message',
                    'transaction_date', 'basket_id', 'email']
    readonly_fields = [
        'user',
        'amount',
        'currency_type',
        'transaction_id',
        'razorpay_id',
        'error_code',
        'error_message',
        'transaction_date',
        'basket_id',
        'email'
    ]

admin.site.register(models.RazorpayTransaction, RazorpayTransactionAdmin)
