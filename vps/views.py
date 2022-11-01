from django.db.models import F, Sum, Case, When, Value, FloatField, ExpressionWrapper, Count, Q
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from practice_1.paginations import VpsLimitOffsetPagination
from vps.filters import VpsFilter
from vps.models import Vps
from vps.serializers import (
    VpsSerializer, VpsStatusSerializer,
    VpsSingleSerializer
)


@extend_schema_view(
    list=extend_schema(description="View all of the existing vps in our system",
                       summary="View vps"),
    create=extend_schema(description="Add new vps to our system",
                         summary="Create new vps"),
    retrieve=extend_schema(description="View specific existing vps in our system",
                           summary="View specific vps"),
    update=extend_schema(description="Updates data about existing vps in our system",
                         summary="Update existing vps"),
    destroy=extend_schema(description="Deletion of existing vps from our system",
                          summary="Delete existing vps")
)
class VpsViewSet(viewsets.ModelViewSet):
    queryset = Vps.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VpsSerializer
    pagination_class = VpsLimitOffsetPagination
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
        if self.request.method == "GET" and self.kwargs.get("pk"):
            return VpsSingleSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            status_count = Vps.objects.all().aggregate(
                started=Count("status", filter=Q(status="started")),
                blocked=Count("status", filter=Q(status="blocked")),
                stopped=Count("status", filter=Q(status="stopped"))
            )
            serializer = self.get_serializer(queryset, many=True)
            status_count["results"] = serializer.data
            return Response(status_count)


@extend_schema_view(
    put=extend_schema(description="This route is used for vps status update only",
                      summary="Vps status update")
)
class VpsStatusUpdateView(UpdateAPIView):
    queryset = Vps.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VpsStatusSerializer
    http_method_names = ["put"]
