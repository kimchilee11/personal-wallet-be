from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, LoginUserViewSet, MoneyViewSet, UserViewSet
from .views import GoogleSocialAuthView
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register('register', RegisterUserViewSet)
router.register('', UserViewSet)
router.register('money', MoneyViewSet)

urlpatterns = [
    path('login/google/', GoogleSocialAuthView.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view()),
]

urlpatterns += router.urls
