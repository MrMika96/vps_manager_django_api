from django.db.models import F, Sum, Case, When, Value, FloatField, ExpressionWrapper
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from vps.filters import VpsFilter
from vps.models import Vps
from vps.serializers import (
    VpsSerializer, VpsStatusSerializer,
    VpsSingleSerializer
)


class VpsViewSet(viewsets.ModelViewSet):
    queryset = Vps.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VpsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VpsFilter

    def get_queryset(self):
        return self.queryset.prefetch_related(
            "maintained_by", "maintained_by__profile", "deployed_applications"
        ).annotate(
            applications_size=Sum("deployed_applications__size", default=0),
            free_space=Case(
                When(applications_size__gt=0,
                     then=ExpressionWrapper(
                         F("hdd")-F("applications_size")/Value(1000, output_field=FloatField()),
                         output_field=FloatField())
                     ),
                default=F("hdd"), output_field=FloatField()),
            free_space_percentage=ExpressionWrapper(
                F("free_space")/F("hdd")*Value(100, output_field=FloatField()),
                output_field=FloatField())
        )

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.kwargs.get('pk'):
            return VpsSingleSerializer
        return self.serializer_class


class VpsStatusUpdateView(UpdateAPIView):
    queryset = Vps.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VpsStatusSerializer
    http_method_names = ["put"]
