from collections import OrderedDict

from django.db.models import Count, Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from vps.models import Vps


class VpsLimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        status_count = Vps.objects.all().aggregate(
            started=Count("status", filter=Q(status="started")),
            blocked=Count("status", filter=Q(status="blocked")),
            stopped=Count("status", filter=Q(status="stopped")),
        )
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("started", status_count["started"]),
                    ("blocked", status_count["blocked"]),
                    ("stopped", status_count["stopped"]),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
