from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import (
    UserTokenObtainPairSerializer, UserRegisterSerializer,
    UserSerializer, UserCredentialsUpdateSerializer
)
from users.utils import return_users_annotated_fields


@extend_schema_view(
    post=extend_schema(description="Takes a set of user credentials and returns "
                                   "an access and refresh JSON web token pair "
                                   "to prove the authentication of those credentials.",
                       summary="User authorization in the system"
                       )
)
class UserAuthView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


@extend_schema_view(
    retrieve=extend_schema(description="Route for viewing your own information",
                           summary="Get authorized user data"),
    update=extend_schema(description="Route for updating your profile information",
                         summary="Update authorized user data"),
    destroy=extend_schema(description="Route for deletion of your own account from system",
                          summary="delete authorized user")
)
class UserMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(
            id=self.request.user.id
        ).select_related(
            "profile"
        ).annotate(
            **return_users_annotated_fields()
        ).first()


@extend_schema_view(
    list=extend_schema(description="Route for viewing all users who have been registered in the system",
                       summary="View all users"),
    retrieve=extend_schema(description="Route for viewing specific users, via user id,  "
                                       "who have been registered in the system",
                           summary="View specific user")
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.select_related(
            "profile"
        ).annotate(
            **return_users_annotated_fields()
        )

    def get_serializer_class(self):
        if self.action == "user_register":
            return UserRegisterSerializer
        if self.action == "user_change_credentials":
            return UserCredentialsUpdateSerializer
        return self.serializer_class

    def get_object(self):
        if self.action == "user_change_credentials":
            return self.request.user
        return super().get_object()

    @extend_schema(
        request=UserRegisterSerializer,
        responses=UserRegisterSerializer,
        summary="User registration in the system",
        description="User system registration, takes users email, "
                    "password and profile data and saves it in our system"
    )
    @action(
        permission_classes=[AllowAny],
        url_path='register',
        url_name='register',
        methods=['post'], detail=False
    )
    def user_register(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        request=UserCredentialsUpdateSerializer,
        responses=UserCredentialsUpdateSerializer,
        summary="Authorized user credentials update",
        description="This route is only for changing authorized user email and password"
    )
    @action(
        url_path='change_credentials',
        url_name='change_credentials',
        methods=['put'], detail=False
    )
    def user_change_credentials(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
