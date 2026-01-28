from rest_framework import serializers
from .models import Receipt, ReceiptItem

class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = ['item_name', 'quantity', 'unit_price']

class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ['receipt_number', 'subtotal', 'tax', 'total']

    def create(self, validated_data):
        items = validated_data.pop('items')
        business = validated_data['business']

        from .utils import generate_receipt_number, check_receipt_limit
        check_receipt_limit(business)

        subtotal = sum(i['quantity'] * i['unit_price'] for i in items)
        tax = subtotal * 0.05
        total = subtotal + tax - validated_data.get('discount', 0)

        receipt = Receipt.objects.create(
            receipt_number=generate_receipt_number(business),
            subtotal=subtotal,
            tax=tax,
            total=total,
            **validated_data
        )

        for item in items:
            ReceiptItem.objects.create(receipt=receipt, **item)

        return receipt
