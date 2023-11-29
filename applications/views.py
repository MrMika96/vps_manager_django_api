from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from applications.models import Application
from applications.serializers import ApplicationSerializer


@extend_schema_view(
    list=extend_schema(description="Shows all applications what been deployed on servers",
                       summary="View all deployed applications"
                       ),
    create=extend_schema(description="Adding applications to system and deploying them to vps",
                         summary="User authorization in the system"
                         ),
    retrieve=extend_schema(description="Route for showing specific application from our system",
                           summary="Show specific application"
                           ),
    update=extend_schema(description="Updates already existing applications from our system",
                         summary="Application update"
                         ),
    destroy=extend_schema(description="Deletes application from servers and system",
                          summary="Application delete"
                          )
)
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.prefetch_related('vps_set')
