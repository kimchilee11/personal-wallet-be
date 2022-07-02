from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import TypeTransactionSerializer, TransactionSerializer, TransactionUpdateSerializer, StatisticSerializer
from .models import Transaction, TypeTransaction
from django.db import transaction
from users.models import User
from .constants import TransStatus
import datetime
import logging
logger = logging.getLogger('ftpuploader')


class TypeTransView(viewsets.ModelViewSet):
    serializer_class = TypeTransactionSerializer
    queryset = TypeTransaction.objects.all()


class StatisticsView(viewsets.ModelViewSet):
    serializer_class = StatisticSerializer
    queryset = Transaction.objects.all()

    def list(self, request, *args, **kwargs):
        account_id = request.user.id
        user_id = User.objects.filter(account_id=account_id).first().id
        transactions = Transaction.objects.filter(user_id=user_id)

        trans_week_1_up = []
        trans_week_1_down = []
        trans_week_2_up = []
        trans_week_2_down = []
        trans_month_1_up = []
        trans_month_1_down = []
        trans_month_2_up = []
        trans_month_2_down = []

        today = datetime.date.today()
        week_day = today.weekday()
        week_day_i = 7 - week_day - 1
        first_day = today + datetime.timedelta(days=-week_day)
        last_day = today + datetime.timedelta(days=week_day_i)

        for tran in transactions:
            typ_up = tran.type.is_increased
            time = tran.created_at

            if time.month == today.month:
                if typ_up:
                    trans_month_1_up.append(float(tran.money))
                else:
                    trans_month_1_down.append(float(tran.money))
            if time.month == today.month - 1:
                if typ_up:
                    trans_month_2_up.append(float(tran.money))
                else:
                    trans_month_2_down.append(float(tran.money))
            # if first_day <= time.date() <= last_day:
            #     if typ_up:
            #         trans_week_1_up.append(float(tran.money))
            #     else:
            #         trans_week_1_down.append(float(tran.money))
            # elif first_day + datetime.timedelta(days=-7) <= time <= last_day - + datetime.timedelta(days=7):
            #     if typ_up:
            #         trans_week_2_up.append(float(tran.money))
            #     else:
            #         trans_week_2_down.append(float(tran.money))

        res_data = {
            # "week": {
            #     "week_1": {
            #         "income": sum(trans_week_1_up),
            #         "expense": sum(trans_week_1_down),
            #     },
            #     "week_2": {
            #         "income": sum(trans_week_2_up),
            #         "expense": sum(trans_week_2_down),
            #     },
            # },
            "month": {
                "month_1": {
                    "income": sum(trans_week_1_up),
                    "expense": sum(trans_week_1_down),
                },
                "month_2": {
                    "income": sum(trans_month_2_up),
                    "expense": sum(trans_month_2_down),
                },
            }
        }

        return Response(res_data, status=status.HTTP_200_OK)


class TransView(viewsets.ModelViewSet):
    serializer_class = TransactionUpdateSerializer
    queryset = Transaction.objects.all()

    def list(self, request, *args, **kwargs):
        account_id = request.user.id
        user_id = User.objects.filter(account_id=account_id).first().id
        trans = Transaction.objects.filter(user_id=user_id).values()
        return Response(trans, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        account_id = request.user.id
        user_info = User.objects.filter(account_id=account_id).first()
        message = {
            "message": ""
        }
        try:
            if user_info:
                data['user'] = user_info.id

                if data['status'] == TransStatus.COMPLETED.name:
                    type_tran = TypeTransaction.objects.filter(id=data['type']).first()
                    type_tran = type_tran.is_increased if type_tran else None
                    if type_tran:
                        change = float(user_info.total_money) + float(data['money'])
                    else:
                        if float(user_info.total_money) < float(data['money']):
                            raise Exception('This transaction is higher than money in your wallet')
                        change = float(user_info.total_money) - float(data['money'])
                    User.objects.update(total_money=change)
                if data:
                    Transaction.objects.create(
                        name=data['name'],
                        money=data['money'],
                        user_id=data['user'],
                        currency_unit=data['currency_unit'],
                        status=data['status'],
                        note=data['note'],
                        type_id=data['type'],
                        created_at=data['created_at']
                    )
            else:
                raise Exception('not exist user')

            message['message'] = 'successful'
        except Exception as e:
            logger.error('Error: ' + str(e))
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
        account_id = request.user.id
        user_info = User.objects.filter(account_id=account_id)
        tran_info = Transaction.objects.filter(id=id_tran)
        message = {"message": ""}

        try:

            if user_info.exists() is not None and tran_info.exists() is not None:
                user_info = user_info.first()
                tran_info = tran_info.first()
                type = TypeTransaction.objects.filter(id=data['type']).first()

                if type and type.is_increased:
                    m = float(user_info.total_money) - float(tran_info.money) + float(data['money'])
                else:
                    m = float(user_info.total_money) + float(tran_info.money) - float(data['money'])

                query_set = Transaction.objects.filter(id=tran_info.id)
                if query_set.exists():
                    query_set.update(
                        name=data['name'],
                        money=data['money'],
                        currency_unit=data['currency_unit'],
                        status=data['status'],
                        type_id=data['type']
                    )
                User.objects.filter(id=user_info.id).update(total_money=m)
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
        account_id = request.user.id
        trans_id = self.kwargs.get('pk')
        user_info = User.objects.filter(account_id=account_id).first()
        tran_info = Transaction.objects.filter(id=trans_id).first()
        message = {
            "message": ""
        }
        try:
            if tran_info.status == TransStatus.COMPLETED.name:
                type_tran = tran_info.type.is_increased
                if type_tran:
                    if float(user_info.total_money) < float(tran_info.money):
                        raise Exception('This transaction is higher than money in your wallet')
                    change = float(user_info.total_money) - float(tran_info.money)
                else:
                    change = float(user_info.total_money) + float(tran_info.money)
            User.objects.filter(id=user_info.id).update(total_money=change)
            Transaction.objects.filter(id=trans_id).delete()
        except Exception as e:
            logger.error('Error: ' + str(e))
            message["message"] = 'Error: ' + str(e)
            transaction.rollback()
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(message, status=status.HTTP_200_OK)


