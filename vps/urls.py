from rest_framework.routers import DefaultRouter

from vps import views


router = DefaultRouter()
router.register(prefix='',
                viewset=views.VpsViewSet,
                basename='vps')

urlpatterns = router.urls
