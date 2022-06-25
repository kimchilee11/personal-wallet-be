from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, LoginUserViewSet, MoneyViewSet, UserViewSet, GoogleSocialAuthView

router = DefaultRouter()
router.register('google', GoogleSocialAuthView)
router.register('login', LoginUserViewSet)
router.register('register', RegisterUserViewSet)
router.register('', UserViewSet)
router.register('money', MoneyViewSet)

# urlpatterns = [
#     path('', GoogleSocialAuthView)
# ]

urlpatterns = router.urls
