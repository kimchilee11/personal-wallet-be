from rest_framework.routers import DefaultRouter

from .views import SavingMoneyView, SavingMoneyTransView

router = DefaultRouter()
router.register(r'trans', SavingMoneyTransView)
router.register(r'', SavingMoneyView)


urlpatterns = router.urls
