from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from applications.models import Application
from applications.serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
