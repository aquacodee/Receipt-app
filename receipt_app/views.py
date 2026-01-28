import uuid
from django.utils.timezone import now, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .paystack import initialize_payment
from rest_framework.viewsets import ModelViewSet
from .models import Receipt,Plan, Subscription, Payment
from .serializers import ReceiptSerializer

from django.http import FileResponse
import os
from django.conf import settings
from .pdf import generate_receipt_pdf

class ReceiptViewSet(ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Receipt.objects.filter(
            business__owner=self.request.user
        )

class UpgradeSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get("plan_id")
        business = request.user.businesses.first()
        plan = Plan.objects.get(id=plan_id)

        reference = str(uuid.uuid4())

        payment = Payment.objects.create(
            business=business,
            amount=plan.price,
            reference=reference,
            status="pending"
        )

        paystack_response = initialize_payment(
            request.user.email,
            plan.price,
            reference
        )
        return Response(paystack_response)


class ReceiptPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        receipt = Receipt.objects.get(pk=pk, business__owner=request.user)
        sub = receipt.business.subscription
        watermark = not sub.plan.has_branding

        file_path = f"{settings.MEDIA_ROOT}/receipt_{receipt.id}.pdf"
        generate_receipt_pdf(receipt, file_path, watermark)

        return FileResponse(open(file_path, 'rb'), as_attachment=True)