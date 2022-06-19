from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer
from .serializers import UserSerializer, RegisterUserSerializer, AccountSerializer, MoneySerializer
from .models import Account, User
from django.db import transaction
import logging
logger = logging.getLogger('ftpuploader')
from django.contrib.auth.hashers import check_password


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        user = None
        if data is not None:
            hi = Account.objects.get_or_create(
                username=data['name'],
                email=data['email'],
                login_with_gg=True
            )
            user_exist = User.objects.get_or_create(
                account=hi[0],
                avatar=data['picture'],
                full_name=data['name'],
                total_money=0
            )
            user = UserSerializer(user_exist[0])
        return Response(user.data['id'], status=status.HTTP_200_OK)


class LoginUserViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        seri = serializer.validated_data
        user_exist = Account.objects.filter(username=seri['username'])
        message = {
            "message": ""
        }
        try:
            if user_exist.exists():
                user_exist = user_exist.first()
                user = AccountSerializer(user_exist)
                user = user.data
                check = check_password(seri['password'], user['password'])
                if check:
                    message["message"] = 'login successful'
                else:
                    message["message"] = 'pls check your password'
            else:
                raise Exception('pls check your username')
        except Exception as e:
            message["message"] = str(e)
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        return Response(message, status=status.HTTP_200_OK)


class RegisterUserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        seri = serializer.validated_data
        data = {
            'password': seri['password'],
            'username': seri['username'],
            'email': seri['email'],
            'avatar': seri['avatar'],
            'full_name': seri['full_name'],
            'address': seri['address'],
            'total_money': 0,
        }
        user = None
        try:
            if data is not None:
                hi = Account.objects.get_or_create(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    login_with_gg=False
                )
                user_exist = User.objects.get_or_create(
                    account=hi[0],
                    avatar=data['avatar'],
                    full_name=data['full_name'],
                    address=data['address'],
                    total_money=0
                )
                user = UserSerializer(user_exist[0])
                user = user.data
        except Exception as e:
            logger.error('Failed to upload to ftp: ' + str(e))
            transaction.rollback()
        return Response(user, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        data = request.data
        print(data)
        if data:
            query_set = User.objects.filter(id=id)
            if query_set.exists():
                query_set.update(
                    avatar=data['avatar'],
                    full_name=data['full_name'],
                    address=data['address'],
                    total_money=data['total_money']
                )
        response = {'message': 'Successful'}
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        query_set = User.objects.filter(id=id)
        query_set = query_set.first()
        user = UserSerializer(query_set)
        return Response(user.data, status=status.HTTP_200_OK)


class MoneyViewSet(viewsets.ModelViewSet):
    serializer_class = MoneySerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        money = int(request.data['total_money'])
        if money >= 0:
            query_set = User.objects.filter(id=id)
            if query_set.exists():
                query_set.update(total_money=money)
        response = {'message': 'Successful'}
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        User.objects.filter(id=id).update(total_money=0)
        return Response('successful', status=status.HTTP_200_OK)
