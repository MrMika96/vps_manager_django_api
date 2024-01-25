from rest_framework.routers import DefaultRouter

from applications import views

app_name = "applications"

router = DefaultRouter()
router.register(prefix="", viewset=views.ApplicationViewSet, basename="applications")

urlpatterns = router.urls
