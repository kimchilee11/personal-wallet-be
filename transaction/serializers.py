from rest_framework import serializers

from .models import TypeTransaction, Transaction


class TypeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTransaction
        fields = ['id', 'type']
