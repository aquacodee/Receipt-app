from django.contrib import admin
from .models import Receipt, ReceiptItem

# Register your models here.
# class ReceiptItemInline(admin.TabularInline):
#     model = ReceiptItem
#     extra = 1

# @admin.register(Receipt)
# class ReceiptAdmin(admin.ModelAdmin):
#     inlines = [ReceiptItemInline]
#     list_display = ('receipt_number', 'business_name', 'total', 'created_at')