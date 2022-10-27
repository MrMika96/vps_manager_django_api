import uuid

from django.db import models

from applications.models import Application
from users.models import User


class Vps(models.Model):
    STATUSES = [
        ("started", "started"),
        ("blocked", "blocked"),
        ("stopped", "stopped"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpu = models.IntegerField()
    ram = models.IntegerField()
    hdd = models.IntegerField()
    status = models.CharField(choices=STATUSES, default="started", max_length=7)
    maintained_by = models.ManyToManyField(User)
    deployed_applications = models.ManyToManyField(Application)
