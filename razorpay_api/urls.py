from django.urls import path, re_path
from . import views

app_name='razorpay_api'

urlpatterns = [
    re_path(r'^preview/(?P<basket_id>\d+)/$',
        views.SuccessResponseView.as_view(),
        name='razorpay-success-response'),
    re_path(r'^cancel/(?P<basket_id>\d+)/(?P<transaction_id>[a-z0-9]{32})$',
    views.CancelResponseView.as_view(),
        name='canceld-request'),
]
