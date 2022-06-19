from django.db import models
from django.contrib.auth.models import AbstractUser
from transaction.constants import ValueCurrency


class Account(AbstractUser):
    username = models.CharField(unique=True, null=False, max_length=50, default='')
    email = models.EmailField(unique=True, null=False, max_length=50, default='')
    created = models.DateTimeField(auto_now_add=True)
    login_with_gg = models.BooleanField(default=False)


class User(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    avatar = models.CharField(null=True, max_length=200)
    full_name = models.CharField(null=False, max_length=50, default='')
    address = models.CharField(null=True, max_length=50)
    total_money = models.DecimalField(max_digits=15, decimal_places=0)
    currency_unit = models.CharField(null=False, max_length=100, choices=ValueCurrency.choices(), default=ValueCurrency.VND)
