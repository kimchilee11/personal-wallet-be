from rest_framework.routers import DefaultRouter

from .views import TypeTransView, TransView, StatisticsView

router = DefaultRouter()
router.register(r'statistics', StatisticsView)
router.register(r'types', TypeTransView)
router.register(r'', TransView)


urlpatterns = router.urls
