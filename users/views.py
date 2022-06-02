from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer


from .serializers import UserSerializer, AccountSerializer
from .models import Account, User


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
        return Response(user.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Destroy function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'Retrieve function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)