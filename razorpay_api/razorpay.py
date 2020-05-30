import logging
from uuid import uuid4
import razorpay
from .models import RazorpayTransaction as IntialTransaction
from django.conf import settings


rz_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
)

def start_transaction(basket, amount, user=None, email=None):
    try:
        if basket.currency:
            currency = basket.currency
        else:
            currency = getattr(settings, 'OSCAR_DEFAULT_CURRENCY', 'INR')
        intial_transaction = IntialTransaction(
            user=user, amount=amount, currency_type=currency, status="initiated",
            basket_id=basket.id, transaction_id=uuid4().hex[:32], email=email
        )
        intial_transaction.save()
        return intial_transaction
    except Exception as e:
        logger.warning('%s', e)


def update_transaction_details(razorpay_id, transaction_id):
    payment = rz_client.payment.fetch(razorpay_id)
    try:
        transaction_details = IntialTransaction.objects.get(
            transaction_id=transaction_id)
    except Exception as e:
        logger.error('Transaction failed update')
    if(int(transaction_details.amount * 100) != payment['amount']
       or transaction_details.currency_type != payment['currency']
       or transaction_id != transaction_details.transaction_id):
        raise Exception
    transaction_details.status = payment["status"]
    transaction_details.razorpay_id = razorpay_id
    transaction_details.save()
    return transaction_details


def capture_transaction(session, rz_id):
    """
    capture the payment
    """
    try:
        txn = IntialTransaction.objects.get(razorpay_id=rz_id)
        rz_client.payment.capture(rz_id, int(txn.amount * 100))
        txn.status = "captured"
        txn.save()
    except Exception as e:
        raise RazorpayError
    return txn
