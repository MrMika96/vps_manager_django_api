from django.db.models import Count, Case, When, CharField, Value
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import (
    UserTokenObtainPairSerializer, UserRegisterSerializer,
    UserSerializer, UserCredentialsUpdateSerializer
)


class UserAuthView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(
            id=self.request.user.id
        ).select_related(
            "profile"
        ).prefetch_related(
            "application_set"
        ).annotate(
            vps_count=Count("vps"),
            workload=Case(
                When(vps_count__range=[1, 3], then=Value("EASY", output_field=CharField())),
                When(vps_count__range=[3, 8], then=Value("MEDIUM", output_field=CharField())),
                When(vps_count__gte=9, then=Value("HARD", output_field=CharField())),
                default=Value("VERY_EASY", output_field=CharField())
            ),
            applications_deployed=Count("application", distinct=True)
        ).first()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.select_related("profile").prefetch_related("application_set").annotate(
            vps_count=Count("vps"),
            workload=Case(
                When(vps_count__range=[1, 3], then=Value("EASY", output_field=CharField())),
                When(vps_count__range=[3, 8], then=Value("MEDIUM", output_field=CharField())),
                When(vps_count__gte=9, then=Value("HARD", output_field=CharField())),
                default=Value("VERY_EASY", output_field=CharField())
            ),
            applications_deployed=Count("application", distinct=True)
        )


class UserCredentialsUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCredentialsUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user
