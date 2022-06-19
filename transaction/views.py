from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import TypeTransactionSerializer, TransactionSerializer, TransactionUpdateSerializer
from .models import Transaction, TypeTransaction
from django.db import transaction
from users.models import User
from users.serializers import UserSerializer
from .constants import TransStatus
import logging
logger = logging.getLogger('ftpuploader')


class TypeTransView(viewsets.ModelViewSet):
    serializer_class = TypeTransactionSerializer
    queryset = TypeTransaction.objects.all()


class TransView(viewsets.ModelViewSet):
    serializer_class = TransactionUpdateSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        id_user = request.user.id
        data['user'] = id_user
        message = {
            "message": ""
        }
        try:
            user_info = User.objects.filter(id=id_user)
            if user_info.exists():
                user_info = user_info.first()
                user_info = UserSerializer(user_info).data

                if data['status'] == TransStatus.COMPLETED.name:
                    type_tran = TypeTransaction.objects.filter(id=data['type'])
                    type_tran = type_tran.first()
                    type_tran = TypeTransactionSerializer(type_tran).data['is_increased']
                    if type_tran:
                        change = float(user_info['total_money']) + float(data['money'])
                    else:
                        if float(user_info['total_money']) < float(data['money']):
                            raise Exception('This transaction is higher than money in your wallet')
                        change = float(user_info['total_money']) - float(data['money'])
                    User.objects.update(total_money=change)
                if data is not None:
                    Transaction.objects.create(
                        name=data['name'],
                        money=data['money'],
                        user_id=data['user'],
                        currency_unit=data['currency_unit'],
                        status=data['status'],
                        note=data['note'],
                        type_id=data['type']
                    )
            else:
                raise Exception('not exist user')

            message['message'] = 'successful'
        except Exception as e:
            logger.error('Error: ' + str(e))
            message["message"] = 'Error: ' + str(e)
            transaction.rollback()
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(message, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id_tran = self.kwargs.get('pk')
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        id_user = request.user.id
        message = {
            "message": ""
        }
        try:
            user_info = User.objects.filter(id=id_user)
            tran_info = Transaction.objects.filter(id=id_tran)

            if user_info.exists() is not None and tran_info.exists() is not None:
                user_info = user_info.first()
                user_info = UserSerializer(user_info).data

                tran_info = tran_info.first()
                tran_info = TransactionUpdateSerializer(tran_info).data

                if data['status'] == TransStatus.COMPLETED.name and tran_info['status'] == TransStatus.PENDING.name:
                    type_tran = TypeTransaction.objects.filter(id=data['type'])
                    type_tran = type_tran.first()
                    type_tran = TypeTransactionSerializer(type_tran).data['is_increased']
                    if type_tran:
                        change = float(user_info['total_money']) + float(data['money'])
                    else:
                        if float(user_info['total_money']) < float(data['money']):
                            raise Exception('This transaction is higher than money in your wallet')
                        change = float(user_info['total_money']) - float(data['money'])
                    User.objects.update(total_money=change)
                if tran_info is not None:
                    query_set = Transaction.objects.filter(id=id_tran)
                    if query_set.exists():
                        print(data)
                        query_set.update(
                            name=data['name'],
                            money=data['money'],
                            currency_unit=data['currency_unit'],
                            status=data['status'],
                            note=data['note'],
                            type_id=data['type']
                        )
            else:
                raise Exception('not exist user')

            message['message'] = 'successful'
        except Exception as e:
            logger.error('Error: ' + str(e))
            message["message"] = 'Error: ' + str(e)
            transaction.rollback()
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(message, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id_user = request.user.id
        id_tran = self.kwargs.get('pk')
        tran_info = Transaction.objects.filter(id=id_tran)
        user_info = User.objects.filter(id=id_user)
        message = {
            "message": ""
        }
        print(user_info)
        try:
            if tran_info.exists():
                tran_info = tran_info.first()
                tran_info = TransactionUpdateSerializer(tran_info).data

                user_info = user_info.first()
                user_info = UserSerializer(user_info).data

                if tran_info['status'] == TransStatus.COMPLETED.name:
                    type_tran = TypeTransaction.objects.filter(id=tran_info['type'])
                    type_tran = type_tran.first()
                    type_tran = TypeTransactionSerializer(type_tran).data['is_increased']
                    if type_tran is False:
                        change = float(user_info['total_money']) + float(tran_info['money'])
                    else:
                        if float(user_info['total_money']) < float(tran_info['money']):
                            raise Exception('This transaction is higher than money in your wallet')
                        change = float(user_info['total_money']) - float(tran_info['money'])
                    User.objects.update(total_money=change)
                Transaction.objects.filter(id=id_tran).delete()
        except Exception as e:
            logger.error('Error: ' + str(e))
            message["message"] = 'Error: ' + str(e)
            transaction.rollback()
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(message, status=status.HTTP_200_OK)