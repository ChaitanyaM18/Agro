import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from oscar.core.loading import get_class, get_model
from django.views.generic import RedirectView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.db.models import Q
from razorpay_api import razorpay

Basket = get_model('basket', 'Basket')
RazorpayTransaction = get_model('razorpay_api', 'RazorpayTransaction')
PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
ShippingAddress = get_model('order', 'ShippingAddress')
Country = get_model('address', 'Country')
Basket = get_model('basket', 'Basket')
Repository = get_class('shipping.repository', 'Repository')
Selector = get_class('partner.strategy', 'Selector')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')

logger = logging.getLogger('kimsecomm.custom.razorpay')

Applicator = get_class('offer.applicator', 'Applicator')

# Create your views here.


class CancelResponseView(RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        basket = get_object_or_404(Basket, id=kwargs['basket_id'],
                                   status=Basket.FROZEN)
        basket.thaw()
        RazorpayTransaction.objects.filter(Q(basket_id=kwargs['basket_id'])
                                           and Q(transaction_id = kwargs['transaction_id'])).update(status='Cancelled by user')
        return super(CancelResponseView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, _("Razorpay transaction cancelled"))
        return reverse('basket:summary')


class SuccessResponseView(PaymentDetailsView):
    preview = True

    @property
    def pre_conditions(self):
        return []

    def get(self, request, *args, **kwargs):
        try:
            self.razorpay_id = request.GET['razorpay_id']
            self.transaction_id = request.GET['transaction_id']
        except Exception as e:
            return HttpResponseRedirect(reverse('basket:summary'))

        try:
            self.transaction_status = razorpay.update_transaction_details(
                self.request.session['selected_hospital'], self.razorpay_id, self.transaction_id)
        except Exception as e:
            logger.warning('%s', e)
            return HttpResponseRedirect(reverse('basket:summary'))

        kwargs['basket'] = self.load_frozen_basket(kwargs['basket_id'])
        if not kwargs['basket']:
            messages.error(
                self.request,
                _("No basket was found that corresponds to your "
                  "Razorpay transaction"))
            return HttpResponseRedirect(reverse('basket:summary'))
        basket = kwargs['basket']
        submission = self.build_submission(basket=basket)
        return self.submit(**submission)

    def load_frozen_basket(self, basket_id):
        try:
            basket = Basket.objects.get(id=basket_id, status=Basket.FROZEN)
        except Basket.DoesNotExist:
            return None
        if Selector:
            basket.strategy = Selector().strategy(self.request)
        Applicator().apply(basket=basket,
                           user=self.request.user, request=self.request)
        return basket

    def build_submission(self, **kwargs):
        submission = super(
            SuccessResponseView, self).build_submission(**kwargs)
        if not self.request.user.is_authenticated():
            submission['order_kwargs']['guest_email'] = self.transaction_status.email
        else:
            submission['order_kwargs']['guest_email'] = ""
        submission['payment_kwargs']['razorpay_id'] = self.razorpay_id
        submission['payment_kwargs']['transaction_id'] = self.transaction_id
        return submission

    def handle_payment(self, order_number, total, **kwargs):
        try:
            confirm_txn = razorpay.capture_transaction(self.request.session['selected_hospital'], kwargs["razorpay_id"])
        except Exception as e:
            raise UnableToTakePayment()
        try:
            if not confirm_txn.is_successful:
                raise UnableToTakePayment()

            # Record payment source and event
            source_type, is_created = SourceType.objects.get_or_create(
                name='Razorpay')
            source = Source(source_type=source_type,
                            currency=confirm_txn.currency_type,
                            amount_allocated=confirm_txn.amount,
                            amount_debited=confirm_txn.amount)
            self.add_payment_source(source)
            self.add_payment_event('Settled', confirm_txn.amount,
                                   reference=confirm_txn.razorpay_id)
        except Exception as e:
            logger.warning('handle payment execption %s', e)
            raise
