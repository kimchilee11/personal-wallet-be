from django.db import models
from users.models import User
from .constants import DailyStatus


class SavingMoney(models.Model):
    name = models.CharField(null=False, default='', max_length=100)
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    money_goal = models.DecimalField(max_digits=20, decimal_places=2)
    saving_money = models.DecimalField(max_digits=20, decimal_places=2)
    daily = models.CharField(null=True, max_length=1000, choices=DailyStatus.choices(), default=DailyStatus.WEEK)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class SaveTrans(models.Model):
    money = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    note = models.CharField(null=False, default='', max_length=100)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    original = models.ForeignKey(SavingMoney, on_delete=models.CASCADE)
