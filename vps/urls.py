from rest_framework.routers import DefaultRouter

from vps import views

app_name = 'vps'


router = DefaultRouter()
router.register(prefix='',
                viewset=views.VpsViewSet,
                basename='vps')

urlpatterns = router.urls
