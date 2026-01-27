from random import choices
from django.db import models

# Create your models here.
class Receipt(models.Model):
    receipt_number = models.CharField(max_length = 20, unique = True)
    business_name = models.CharField(max_length=250)
    business_phone = models.CharField(max_length=250, blank=True)
    customer_name = models.CharField(max_length=200, blank=True)
    payment_method = models.CharField(
        max_length=20,
        choices =[
            ('cash', 'Cash'),
            ('momo', 'Mobile Money'),
            ('card', 'Card'),
        ]
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.receipt_number}"

class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        related_name="items",
        on_delete=models.CASCADE
    )
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item_name
