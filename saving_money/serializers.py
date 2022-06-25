from rest_framework import serializers

from .models import SavingMoney, SaveTrans


class SavingMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingMoney
        fields = ['id', 'name', 'budget', 'money_goal', 'saving_money', 'daily', 'user', 'status']
        depth = 1


class SavingMoneyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingMoney
        fields = ['id', 'name', 'budget', 'money_goal', 'saving_money', 'daily', 'status']


class SavingMoneyTransSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=False)

    class Meta:
        model = SaveTrans
        fields = ['id', 'money', 'note', 'original', 'status']
        depth = 0
