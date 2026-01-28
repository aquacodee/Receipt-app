import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.timezone import now, timedelta
from .models import Payment, Subscription, Plan

@csrf_exempt
def paystack_webhook(request):
    payload = json.loads(request.body)
    event = payload.get("event")

    if event == "charge.success":
        data = payload["data"]
        reference = data["reference"]

        payment = Payment.objects.get(reference=reference)
        payment.status = "success"
        payment.save()

        business = payment.business
        plan = Plan.objects.get(price=payment.amount)

        Subscription.objects.update_or_create(
            business=business,
            defaults={
                "plan": plan,
                "expires_at": now() + timedelta(days=30),
                "is_active": True
            }
        )

    return HttpResponse(status=200)