from oscar.apps.checkout.views import PaymentDetailsView as PaymentDetailView
from razorpay_api import razorpay
from django.conf import settings

class PaymentDetailsView(PaymentDetailView):
    def start_payment(self):
        basket = self.build_submission()['basket']
        basket.freeze()
        order_total = self.build_submission()['order_total']
        amount = order_total.incl_tax
        if self.request.user.is_authenticated:
            email = self.request.user.email
            user = self.request.user
        else:
            email = self.build_submission()['order_kwargs']['guest_email']
            user = None
        transaction = razorpay.start_transaction(basket, amount, user, email)
        rz_key = settings.RAZORPAY_API_KEY
        print(amount)
        context = {

            "amount": int(amount * 100),  # amount in paisa as int
            "rz_key": rz_key,
            "email": email,
            "txn_id": transaction.transaction_id,
            "name": getattr(settings, "OSCAR_SHOP_NAME", " "),
            "theme_color": getattr(
                settings, "RAZORPAY_THEME_COLOR", "#ff9600"
            ),
            "logo_url": getattr(
                settings, "RAZORPAY_VENDOR_LOGO",
                ""),
        }
        return context

    def get_context_data(self, **kwargs):
        context = super(PaymentDetailsView, self).get_context_data(**kwargs)
        if not self.preview:
            context = self.start_payment()
            return context
        else:
            return context
