from rest_framework import serializers

from users.models import User
from users.serializers import MaintainerSerializer
from vps.models import Vps


class VpsSerializer(serializers.ModelSerializer):
    cpu = serializers.IntegerField(
        min_value=4,
        max_value=256,
        help_text="Gigabytes"
    )
    ram = serializers.IntegerField(
        min_value=4,
        max_value=6000,
        help_text="Gigabytes"
    )
    hdd = serializers.IntegerField(
        min_value=16,
        max_value=16000,
        help_text="Gigabytes"
    )
    maintained_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        many=True,
        required=False
    )
    maintainers = MaintainerSerializer(
        source='maintained_by',
        many=True,
        read_only=True,
        default=[]
    )

    class Meta:
        model = Vps
        fields = [
            "id", "ram", "cpu",
            "hdd", "status", "maintainers",
            "maintained_by"
        ]
        read_only_fields = [
            "status"
        ]

    def create(self, validated_data):
        new_vps = super(VpsSerializer, self).create(validated_data)
        new_vps.maintained_by.set(self.validated_data.get('maintained_by'))
        return new_vps

    def update(self, instance, validated_data):
        vps = super(VpsSerializer, self).update(instance=instance, validated_data=validated_data)
        vps.maintained_by.set(self.validated_data.get('maintained_by'))
        return vps


class VpsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vps
        fields = ["status"]
        write_only_fields = ["status"]
