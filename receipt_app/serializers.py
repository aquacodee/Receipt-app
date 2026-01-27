from rest_framework import serializers
from rest_framework import serializers
from .models import Receipt, ReceiptItem

class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        receipt = Receipt.objects.create(**validated_data)

        for item in items_data:
            ReceiptItem.objects.create(receipt=receipt, **item)

        return receipt
