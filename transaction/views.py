from rest_framework import viewsets

from .models import TypeTransaction
from .serializers import TypeTransactionSerializer


class TypeTransView(viewsets.ModelViewSet):
    queryset = TypeTransaction.objects.all()
    serializer_class = TypeTransactionSerializer

