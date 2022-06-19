from django.db import models
from users.models import User
from .constants import ValueCurrency, TransStatus


class TypeTransaction(models.Model):
    type = models.CharField(null=False, max_length=50, default='')
    is_increased = models.BooleanField(default=False)


class Transaction(models.Model):
    name = models.CharField(null=True, max_length=1000)
    money = models.DecimalField(max_digits=20, decimal_places=2)
    currency_unit = models.CharField(null=False, max_length=100, choices=ValueCurrency.choices(), default=ValueCurrency.VND)
    type = models.ForeignKey(TypeTransaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(null=True, max_length=1000, choices=TransStatus.choices(), default=TransStatus.COMPLETED)
    note = models.CharField(null=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

