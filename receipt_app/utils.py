from django.core.exceptions import PermissionDenied
from django.utils.timezone import now
from .models import Receipt

def generate_receipt_number(business):
    count = Receipt.objects.filter(business=business).count() + 1
    return f"{business.id}-RCP-{count:05d}"

def check_receipt_limit(business):
    sub = business.subscription

    if not sub or not sub.is_active:
        raise PermissionDenied("Subscription inactive")

    if sub.expires_at < now():
        raise PermissionDenied("Subscription expired")

    limit = sub.plan.receipt_limit
    if limit != 0:
        if business.receipts.count() >= limit:
            raise PermissionDenied("Receipt limit reached. Upgrade plan.")
