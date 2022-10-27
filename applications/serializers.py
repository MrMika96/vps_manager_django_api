from rest_framework import serializers

from applications.models import Application
from vps.models import Vps


class ApplicationSerializer(serializers.ModelSerializer):
    deployer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    size = serializers.FloatField(min_value=0.0024, max_value=70000.0, required=True)
    deployed_to = serializers.PrimaryKeyRelatedField(
        source="vps_set",
        queryset=Vps.objects.all(),
        required=False,
        many=True
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

    def create(self, validated_data):
        validated_data.pop("vps_set")
        new_app = super(ApplicationSerializer, self).create(validated_data)
        new_app.vps_set.set(self.validated_data.get('vps_set'))
        return new_app

    def update(self, instance, validated_data):
        validated_data.pop("vps_set")
        app = super(ApplicationSerializer, self).update(instance=instance, validated_data=validated_data)
        app.vps_set.set(self.validated_data.get('vps_set'))
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
