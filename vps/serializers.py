from rest_framework import serializers

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

    class Meta:
        model = Vps
        fields = [
            "id", "ram", "cpu",
            "hdd", "status"
        ]
        read_only_fields = [
            "status"
        ]


class VpsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vps
        fields = ["status"]
        write_only_fields = ["status"]
