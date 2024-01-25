from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users import views

app_name = "users"

router = DefaultRouter()

router.register(prefix="", viewset=views.UserViewSet)

urlpatterns = [
    path(
        "me/",
        views.UserMeViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="user_personal_data",
    ),
    path("auth/", views.UserAuthView.as_view(), name="user_auth"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="user_auth_refresh"),
]

urlpatterns += router.urls
