from rest_framework import serializers

from problem_randomizer_be.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "password"]
        # fields = ["username", "name", "url", "password"]

        extra_kwargs = {
            # "url": {"view_name": "api:user-detail", "lookup_field": "username", "read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_password(self, value):
        # Password must be at least 8 characters long
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        # Password must contain at least one digit
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit")
        # Password must contain at least one uppercase letter
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        return value

    def validate_username(self, value):
        # Username must be at least 5 characters long
        if len(value) < 5:
            raise serializers.ValidationError("Username must be at least 5 characters long")
        # Username must be unique
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username must be unique")
        return value
