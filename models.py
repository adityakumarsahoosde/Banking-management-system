from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import uuid


class Account(models.Model):

    ACCOUNT_TYPE = (
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.UUIDField(default=uuid.uuid4, editable=False)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE, default="Savings")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.account_number)

class Transaction(models.Model):

    TRANSACTION_TYPE = (
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer', 'Transfer'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    receiver_account = models.CharField(max_length=50, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"