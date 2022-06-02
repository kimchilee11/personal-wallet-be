from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TypeTransView

router = DefaultRouter()
router.register('', TypeTransView)


urlpatterns = [
    path('types/', include(router.urls)),
]
