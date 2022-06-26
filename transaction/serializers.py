from rest_framework import serializers

from .models import TypeTransaction, Transaction


class TypeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTransaction
        fields = ['id', 'type', 'is_increased']


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.IntegerField()
    user = serializers.IntegerField(default=0)
    note = serializers.CharField(default='ok', max_length=1000)

    class Meta:
        model = Transaction
        fields = ['id', 'name', 'money', 'type', 'user', 'status', 'note', 'currency_unit', 'created_at']
        depth = 1


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'money', 'type', 'user', 'status', 'note', 'currency_unit', 'created_at']


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'money', 'type', 'currency_unit', 'created_at']
        depth = 1
