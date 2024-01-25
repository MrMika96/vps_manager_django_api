import uuid

from django.db import models

from vps_manager_django_api.settings import AUTH_USER_MODEL


class Vps(models.Model):
    STATUSES = [
        ("started", "started"),
        ("blocked", "blocked"),
        ("stopped", "stopped"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpu = models.PositiveIntegerField()
    ram = models.PositiveIntegerField()
    hdd = models.PositiveIntegerField()
    status = models.CharField(choices=STATUSES, default="started", max_length=7)
    maintained_by = models.ManyToManyField(AUTH_USER_MODEL)
    deployed_applications = models.ManyToManyField("applications.Application")
