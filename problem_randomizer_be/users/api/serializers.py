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
