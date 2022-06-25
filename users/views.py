from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from personalWallet import settings
from .serializers import GoogleSocialAuthSerializer
from .serializers import UserSerializer, RegisterUserSerializer, AccountSerializer, MoneySerializer, AccountGGSerializer
from .models import Account, User
from django.db import transaction
import logging

logger = logging.getLogger('ftpuploader')


class GoogleSocialAuthView(viewsets.ModelViewSet):
    serializer_class = GoogleSocialAuthSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        print('hee')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        print(data)
        data['password']=''
        data['address']=''
        user = None
        try:
            if data is not None:
                hi = Account.objects.get_or_create(
                    username=data['name'],
                    email=data['email'],
                    password=data['password'],
                    login_with_gg=True
                )
                print(hi)
                user = User.objects.get_or_create(
                    account=hi[0],
                    avatar=data['picture'],
                    full_name=data['name'],
                    address=data['address'],
                    total_money=0
                )
                print(user)
                user = UserSerializer(user[0])
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Failed to register user: ' + str(e))
            response = {'message': 'Your username and email must be unique'}
            transaction.rollback()
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'error_message': 'Your auth token is invalid!',
            'error_code': 401
        }, status=status.HTTP_401_UNAUTHORIZED)


class LoginUserViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            seri = serializer.validated_data
            user = authenticate(
                request,
                username=seri['username'],
                password=seri['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


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
        response = {'message': 'Successful'}
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
            logger.error('Failed to register user: ' + str(e))
            response = {'message': 'Your username and email must be unique'}
            transaction.rollback()
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        return Response(response, status=status.HTTP_200_OK)


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

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        user_info = Account.objects.filter(id=user_id).first()
        user_info = User.objects.filter(account=user_info).first()
        if user_info:
            user_info = UserSerializer(user_info).data
            return Response(user_info, status=status.HTTP_200_OK)
        message = {
            "message": "Not found user",
        }
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)


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
