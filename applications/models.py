from django.db import models

from vps_manager_django_api.settings import AUTH_USER_MODEL


class Application(models.Model):
    title = models.CharField(max_length=64)
    deployer = models.ForeignKey(AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    size = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deployed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "applications"
        ordering = ["title"]
