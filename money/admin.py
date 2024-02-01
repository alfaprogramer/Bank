from django.contrib import admin
from .models import UserProfile, Transaction, BankAccount, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'mobile_number', 'address', 'mcode']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'amount', 'timestamp']

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

@admin.register(Notification)
class Notification(admin.ModelAdmin):
    list_display=['user', 'message', 'serial_number', 'timestamp','read']
