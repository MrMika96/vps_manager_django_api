from rest_framework import serializers

from applications.serializers import ApplicationShortSerializer
from users.models import User
from users.serializers import MaintainerSerializer
from vps.models import Vps


class VpsSerializer(serializers.ModelSerializer):
    cpu = serializers.IntegerField(
        min_value=4,
        max_value=256,
        help_text="Number of CPU cores"
    )
    ram = serializers.IntegerField(
        min_value=4,
        max_value=6000,
        help_text="RAM value in gigabytes"
    )
    hdd = serializers.IntegerField(
        min_value=16,
        max_value=16000,
        help_text="HDD value in gigabytes"
    )
    maintained_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        many=True,
        required=False,
        help_text="Ids of users who will maintain the server"
    )
    maintainers = MaintainerSerializer(
        source='maintained_by',
        many=True,
        read_only=True,
        default=[],
        help_text="Users who maintain the server"
    )
    free_space = serializers.FloatField(
        read_only=True,
        help_text="Free space of servers hdd (in gigabytes)"
    )
    free_space_percentage = serializers.FloatField(
        read_only=True,
        help_text="Free space of server's hdd in percentages"
    )
    applications_size = serializers.FloatField(
        read_only=True,
        help_text="Space on the server's hdd occupied by applications (in megabytes)"
    )

    class Meta:
        model = Vps
        fields = [
            "id", "ram", "cpu",
            "hdd", "status", "maintainers",
            "maintained_by", "free_space",
            "free_space_percentage", "applications_size"
        ]
        read_only_fields = [
            "status"
        ]

    def create(self, validated_data):
        new_vps = super(VpsSerializer, self).create(validated_data)
        new_vps.maintained_by.set(self.validated_data.get("maintained_by"))
        return new_vps

    def update(self, instance, validated_data):
        vps = super(VpsSerializer, self).update(instance=instance, validated_data=validated_data)
        vps.maintained_by.set(self.validated_data.get("maintained_by"))
        return vps


class VpsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vps
        fields = ["status"]
        write_only_fields = ["status"]


class VpsSingleSerializer(serializers.ModelSerializer):
    maintainers = MaintainerSerializer(
        source="maintained_by",
        many=True,
        read_only=True,
        default=[]
    )
    free_space = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    free_space_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    applications_size = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    deployed_applications = ApplicationShortSerializer(many=True, read_only=True, default=[])

    class Meta:
        model = Vps
        fields = [
            "id", "ram", "cpu",
            "hdd", "status", "maintainers",
            "free_space", "free_space_percentage",
            "applications_size", "deployed_applications"
        ]
        read_only_fields = [
            "id", "ram", "cpu",
            "hdd", "status"
        ]
