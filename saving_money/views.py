from rest_framework import viewsets
from .serializers import SavingMoneySerializer, SavingMoneyTransSerializer
from .models import SavingMoney, SaveTrans
from users.models import User, Account
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('ftpuploader')


class SavingMoneyView(viewsets.ModelViewSet):
    serializer_class = SavingMoneySerializer
    queryset = SavingMoney.objects.all()

    def list(self, request, *args, **kwargs):
        account_id = request.user.id
        user_info = User.objects.filter(account_id=account_id).first()
        tran_info = SavingMoney.objects.filter(user=user_info.id).values()
        tran_info = [dict(q) for q in tran_info]

        data = {
            "box_money": tran_info,
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        trans_id = self.kwargs.get('pk')
        tran_info = SavingMoney.objects.filter(id=trans_id).first()
        tran_info = SavingMoneySerializer(tran_info).data
        data = {
            "saving_money": tran_info,
            "trans_saving_money": []
        }
        if tran_info is None:
            message = {
                "message": "Note found saving money transaction"
            }
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        trans = SaveTrans.objects.filter(original=trans_id).values()
        data["trans_saving_money"] = trans
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        account_id = request.user.id
        user_info = User.objects.filter(account_id=account_id).first()
        seri = self.serializer_class(data=request.data)
        seri.is_valid(raise_exception=True)
        data = seri.validated_data
        data['user'] = user_info.id

        money = None
        try:
            if data:
                money = SavingMoney.objects.get_or_create(
                    name=data['name'],
                    budget=data['budget'],
                    money_goal=data['money_goal'],
                    saving_money=data['saving_money'],
                    daily=data['daily'],
                    user_id=data['user']
                )
                money = SavingMoneySerializer(money[0])
        except Exception as e:
            logger.error('Failed to upload to ftp: ' + str(e))
            transaction.rollback()
        return Response(money.data, status=status.HTTP_200_OK)


class SavingMoneyTransView(viewsets.ModelViewSet):
    serializer_class = SavingMoneyTransSerializer
    queryset = SaveTrans.objects.all()

    def create(self, request, *args, **kwargs):
        seri = self.serializer_class(data=request.data)
        seri.is_valid(raise_exception=True)
        data = seri.validated_data
        account_id = request.user.id
        user_info = User.objects.filter(account_id=account_id).first()
        money_user = float(user_info.total_money) - float(data['money'])

        money = None
        if data['money'] > 0 and money_user >= 0:
            data['status'] = True
        try:
            transaction.set_autocommit(autocommit=False)
            if data:
                money = SaveTrans.objects.get_or_create(
                    money=data['money'],
                    note=data['note'],
                    status=data['status'],
                    original=data['original'],
                )
                original = data['original']
                money_update = float(original.budget) + float(data['money'])
                sta = False
                if float(money_update) >= float(original.money_goal):
                    sta = True

                SavingMoney.objects.filter(id=original.id).update(
                    budget=money_update,
                    status=sta
                )
                user = User.objects.filter(id=user_info.id)
                if money_user < 0:
                    raise "Your wallet don't have enough money to implement transaction"
                user.update(
                    total_money=money_user
                )
            transaction.commit()

        except Exception as e:
            logger.error('Failed to : ' + str(e))
            transaction.rollback()
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('successful', status=status.HTTP_200_OK)
