from django.db import models
from users.models import User


class TypeTransaction(models.Model):
    type = models.CharField(null=False, max_length=50, default='')


class Transaction(models.Model):
    money = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.OneToOneField(TypeTransaction, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(null=True, max_length=50)
    note = models.CharField(null=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

