from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.views.generic import TemplateView
from .views import GoogleSocialAuthView

router = DefaultRouter()
router.register('register', UserViewSet)

urlpatterns = [
    path('login/google/', GoogleSocialAuthView.as_view()),


    path('', TemplateView.as_view(template_name="login_with_gg.html")),
    path('login/', TemplateView.as_view(template_name="signin.html")),
    path('accounts/', include('allauth.urls')),
]