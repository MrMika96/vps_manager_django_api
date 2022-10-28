from django.db import models

from users.models import User


class Application(models.Model):
    title = models.CharField(max_length=64)
    deployer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    size = models.FloatField()
    deployed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "applications"
        ordering = ["title"]
