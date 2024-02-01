from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,BaseUserManager, PermissionsMixin




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    mcode = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
       # Existing fields
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # New fields with default values
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions', default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} sent {self.amount} to {self.receiver} on {self.timestamp}"

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def __str__(self):
        return f"{self.user.username}'s Bank Account"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    serial_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Add this line


    def __str__(self):
        return f"{self.user.username}: {self.message}"
