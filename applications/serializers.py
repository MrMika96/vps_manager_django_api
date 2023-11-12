from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from applications.models import Application
from vps.models import Vps


class ApplicationSerializer(serializers.ModelSerializer):
    deployer = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        help_text="Shows who deployed this application to server"
    )
    size = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0.0024,
        max_value=70000.0,
        required=True,
        help_text="Shows how much space the application would take "
                  "up on the server's hdd (un megabytes)"
    )
    deployed_to = serializers.PrimaryKeyRelatedField(
        source="vps_set",
        queryset=Vps.objects.all(),
        required=False,
        many=True,
        help_text="Shows on which server the application was deployed"
    )

    class Meta:
        model = Application
        fields = [
            "id", "title", "deployer",
            "size", "deployed_at", "updated_at", "deployed_to"
        ]
        read_only_fields = [
            "deployed_at", "updated_at"
        ]

    def validate_deployed_to(self, deployed_to):
        vps_with_filled_hdd = []
        if deployed_to:
            for vps in deployed_to:
                applications_size = sum(
                    list(
                        vps.deployed_applications.values_list("size", flat=True))
                ) + self.initial_data["size"]
                if (vps.hdd - applications_size/1000) <= 0:
                    vps_with_filled_hdd.append(str(vps.id))
        if vps_with_filled_hdd:
            raise ValidationError(detail=f"This servers don`t have enough "
                                         f"free space on their hdd: {vps_with_filled_hdd}")
        return deployed_to

    def create(self, validated_data):
        validated_data.pop("vps_set")
        new_app = super(ApplicationSerializer, self).create(validated_data)
        new_app.vps_set.set(self.validated_data.get("vps_set"))
        return new_app

    def update(self, instance, validated_data):
        validated_data.pop("vps_set")
        app = super(ApplicationSerializer, self).update(instance=instance, validated_data=validated_data)
        app.vps_set.set(self.validated_data.get("vps_set"))
        return app


class ApplicationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id", "title",
            "deployed_at", "updated_at"
        ]
        read_only_fields = [
            "id", "title",
            "deployed_at", "updated_at"
        ]
