from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ReceiptViewSet,
    UpgradeSubscriptionView,
    ReceiptPDFView,
)
from .webhooks import paystack_webhook

router = DefaultRouter()
router.register(r'receipts', ReceiptViewSet, basename='receipt')

urlpatterns = [
    path('upgrade/', UpgradeSubscriptionView.as_view()),
    path('receipt/<int:pk>/pdf/', ReceiptPDFView.as_view()),
    path('paystack/webhook/', paystack_webhook),
]

urlpatterns += router.urls
