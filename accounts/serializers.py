from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "average_rating",
            "phone_number",
            "bio",
            "city",
            "address",
            "profile_picture",
            "is_verified"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        profile_picture = data.get("profile_picture")

        if request and profile_picture and not str(profile_picture).startswith("http"):
            data["profile_picture"] = request.build_absolute_uri(profile_picture)

        return data


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "phone_number",
            "city"
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "phone_number": {
                "validators": [
                    RegexValidator(
                        regex=r'^\+?1?\d{9,15}$',
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        required=False,
        allow_blank=True
    )
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)
    confirm_password = serializers.CharField(write_only=True, required=False, allow_blank=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "bio",
            "city",
            "address",
            "profile_picture",
            "password",
            "confirm_password",
            "email",
        ]
        read_only_fields = ["email"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password or confirm_password:
            if not password or not confirm_password:
                raise serializers.ValidationError(
                    {"password": "Both password and confirm_password are required."}
                )
            if password != confirm_password:
                raise serializers.ValidationError(
                    {"confirm_password": "Passwords do not match."}
                )

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("confirm_password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance