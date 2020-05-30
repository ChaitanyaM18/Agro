from django.db import models
from uuid import uuid4
from django.conf import settings
from django.utils.translation import gettext as _


def generate_id():
    return uuid4().hex[:32]

# Create your models here.


class RazorpayTransaction(models.Model):
    TRANSACTION_INITIATED, TRANSACTION_CAPTURED, TRANSACTION_AUTHORIZED, TRANSACTION_FAILED, AUTHENTICATION_FAILED = (
        "initiated", "captured", "authorized", "capfailed", "authfailed"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    transaction_date = models.DateField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)
    basket_id = models.CharField(
        max_length=15, null=True, blank=True, db_index=True
    )
    currency_type = models.CharField(max_length=15, null=True, blank=True)

    status = models.CharField(max_length=50)

    razorpay_id = models.CharField(
        max_length=22, null=True, blank=True, db_index=True
    )

    error_code = models.CharField(max_length=255, null=True, blank=True)

    error_message = models.CharField(max_length=256, null=True, blank=True)
    transaction_id = models.CharField(
        max_length=64, db_index=True, default=generate_id
    )

    class Meta:
        ordering = ('-transaction_date',)
        app_label = 'razorpay_api'

    @property
    def is_successful(self):
        return self.status == self.TRANSACTION_CAPTURED

    @property
    def is_pending(self):
        return self.status == self.TRANSACTION_AUTHORIZED

    @property
    def is_failed(self):
        return self.status not in (
            self.TRANSACTION_CAPTURED, self.TRANSACTION_AUTHORIZED, self.TRANSACTION_INITIATED
        )

    def __str__(self):
        return 'Razorpay Payment id is : %s' % self.razorpay_id
