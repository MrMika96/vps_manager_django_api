import datetime

from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from users.models import User, Profile


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        self.user = get_object_or_404(User, email=attrs["email"])
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise NotFound(detail="User not found")
        return email

    def validate_password(self, password):
        user = get_object_or_404(User, email=self.initial_data["email"])
        if not user.check_password(password):
            raise ValidationError(detail="Incorrect password")
        return password


class ProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "phone",
            "birth_date",
            "age",
        ]

    def validate(self, attrs):
        if attrs.get("phone"):
            attrs["phone"] = self.Meta.model.normalize_phone(attrs["phone"])
        return attrs

    @extend_schema_field({"type": "string"})
    def get_age(self, obj):
        return (
            datetime.datetime.utcnow().year - obj.birth_date.year
            if obj.birth_date
            else ""
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "password", "profile"]
        read_only_fields = ["id"]

    def validate_email(self, email):
        if self.Meta.model.objects.filter(email=email).exists():
            raise ValidationError(detail="User with that email already exists")
        return self.Meta.model.objects.normalize_email(email)

    def create(self, validated_data):
        return User.objects.register(
            email=validated_data["email"],
            password=validated_data["password"],
            profile=validated_data["profile"],
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(help_text="Contains user's personal data")
    workload = serializers.CharField(
        default=None,
        read_only=True,
        help_text="Displays users workload (how many servers he/she maintaining)",
    )
    applications_deployed = serializers.IntegerField(
        default=0,
        read_only=True,
        help_text="Shows how many applications was deployed to the various servers by this user",
    )

    class Meta:
        model = User
        fields = ["id", "email", "profile", "workload", "applications_deployed"]
        read_only_fields = ["id", "email"]

    def update(self, instance, validated_data):
        super().update(instance.profile, validated_data.pop("profile"))
        return instance


class UserCredentialsUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        help_text="This field is required for password changing. "
        "Field should contain new password",
    )
    old_password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        help_text="This field is required for password changing. "
        "Field should contain old password",
    )

    class Meta:
        model = User
        fields = ["email", "password", "old_password"]

    def validate_email(self, email):
        if self.Meta.model.objects.filter(email=email).exists():
            raise ValidationError("User with that email already exists")
        return self.Meta.model.objects.normalize_email(email)

    def validate_password(self, password):
        if self.initial_data.get("old_password") and self.context[
            "request"
        ].user.check_password(self.initial_data["old_password"]):
            if password and self.initial_data["old_password"] == password:
                raise ValidationError("New password is the same as an old one")
            elif not password and self.initial_data["old_password"] == password:
                raise ValidationError("To change password you must enter new one")
        elif self.initial_data.get("old_password") and not self.context[
            "request"
        ].user.check_password(self.initial_data["old_password"]):
            raise ValidationError("Old password you entered was incorrect")
        return password

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        if validated_data.get("password") and validated_data.get("old_password"):
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


class MaintainerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="profile.first_name", read_only=True)
    last_name = serializers.CharField(source="profile.last_name", read_only=True)
    phone = serializers.CharField(source="profile.phone", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "first_name", "last_name"]
