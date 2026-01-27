from django.db import models

# Create your models here.
class Receipt(models.Model):
    receipt_number = models.CharField(max_length = 20, unique = True)
    business_name = models.CharField(max_length=250)
    business_phone = models.CharField(max_length=250, blank=True)
    customer_name = models.CharField(max_length=200, blank=True)
    payment_method = models.CharField(max_length = 20, choice = [("cash" : "Cash"), ('momo' : "Mobile Money"), ('bank': "Bank")])

