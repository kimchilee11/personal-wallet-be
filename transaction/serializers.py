from rest_framework import serializers

from .models import TypeTransaction, Transaction


class TypeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTransaction
        fields = ['id', 'type', 'is_increased']


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.IntegerField()
    user = serializers.IntegerField(default=0)

    class Meta:
        model = Transaction
        fields = ['id', 'name', 'money', 'type', 'user', 'status', 'note', 'currency_unit']
        depth = 1


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'name', 'money', 'type', 'user', 'status', 'note', 'currency_unit']
        # depth = 1
