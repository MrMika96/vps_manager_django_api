from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from vps.models import Vps
from vps.serializers import VpsSerializer, VpsStatusSerializer


class VpsViewSet(viewsets.ModelViewSet):
    queryset = Vps.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VpsSerializer


class VpsStatusUpdateView(UpdateAPIView):
    queryset = Vps.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VpsStatusSerializer
    http_method_names = ["put"]
