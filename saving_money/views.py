from rest_framework import viewsets
from .serializers import SavingMoneySerializer, SavingMoneyTransSerializer
from .models import SavingMoney, SaveTrans
from users.models import User
from users.serializers import UserSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('ftpuploader')


class SavingMoneyView(viewsets.ModelViewSet):
    serializer_class = SavingMoneySerializer
    queryset = SavingMoney.objects.all()

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        seri = self.serializer_class(data=request.data)
        seri.is_valid(raise_exception=True)
        data = seri.validated_data
        data['user'] = user_id

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
                money = money.data
        except Exception as e:
            logger.error('Failed to upload to ftp: ' + str(e))
            transaction.rollback()
        return Response(money, status=status.HTTP_200_OK)


class SavingMoneyTransView(viewsets.ModelViewSet):
    serializer_class = SavingMoneyTransSerializer
    queryset = SaveTrans.objects.all()

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        seri = self.serializer_class(data=request.data)
        seri.is_valid(raise_exception=True)
        data = seri.validated_data
        user = User.objects.filter(id=user_id).first()
        money_user = float(UserSerializer(user).data['total_money']) - float(data['money'])

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
                money = SavingMoneyTransSerializer(money[0])
                money = money.data

            if data['original']:
                money_update = float(SavingMoneySerializer(data['original']).data['budget']) + float(data['money'])
                up_money = SavingMoneySerializer(data['original']).data
                up_money['budget'] = money_update
                if float(up_money['budget']) > float(up_money['money_goal']):
                    up_money['status'] = True

                SavingMoney.objects.filter(id=up_money['id']).update(
                    budget=up_money['budget'],
                    status=up_money['status']
                )
                print(data)
                user = User.objects.filter(id=user_id)
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

        return Response(money, status=status.HTTP_200_OK)
