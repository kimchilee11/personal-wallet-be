from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import TypeTransactionSerializer, TransactionSerializer, TransactionUpdateSerializer, StatisticSerializer
from .models import Transaction, TypeTransaction
from django.db import transaction
from users.models import User
from users.serializers import UserSerializer
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
        user_id = request.user.id
        tran_info = Transaction.objects.filter(user_id=user_id)
        tran_list = list(tran_info)

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

        for i in tran_list:
            seri_tran = StatisticSerializer(i).data
            typ_up = TypeTransactionSerializer(seri_tran['type']).data['is_increased']
            date = datetime.datetime.strptime(seri_tran['created_at'][2:10], '%y-%m-%d').date()
            time = datetime.date(date.year, date.month, date.day)

            if time.month == today.month:
                if typ_up:
                    trans_month_1_up.append(float(seri_tran['money']))
                else:
                    trans_month_1_down.append(float(seri_tran['money']))
            if time.month == today.month - 1:
                if typ_up:
                    trans_month_2_up.append(float(seri_tran['money']))
                else:
                    trans_month_2_down.append(float(seri_tran['money']))
            if first_day <= time <= last_day:
                if typ_up:
                    trans_week_1_up.append(float(seri_tran['money']))
                else:
                    trans_week_1_down.append(float(seri_tran['money']))
            elif first_day + datetime.timedelta(days=-7) <= time <= last_day - + datetime.timedelta(days=7):
                if typ_up:
                    trans_week_2_up.append(float(seri_tran['money']))
                else:
                    trans_week_2_down.append(float(seri_tran['money']))

        res_data = {
            "week": {
                "week_1": {
                    "income": sum(trans_week_1_up),
                    "expense": sum(trans_week_1_down),
                },
                "week_2": {
                    "income": sum(trans_week_2_up),
                    "expense": sum(trans_week_2_down),
                },
            },
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


