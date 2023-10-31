from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views

app_name = 'users'

router = DefaultRouter()
router.register(prefix='',
                viewset=views.UserViewSet)

urlpatterns = [
    *router.get_urls(),

    path("me", views.UserMeViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    }), name="personal_actions_of_the_client"),
    path("auth", views.UserAuthView.as_view(), name="user_auth"),
    path("register", views.UserRegisterView.as_view(), name="user_register"),
    path("change_credentials", views.UserCredentialsUpdateView.as_view())
]