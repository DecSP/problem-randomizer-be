from rest_framework import serializers

from .models import Contest


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = [
            "id",
            "title",
            "description",
            "duration",
            "start_time",
            "is_public",
            "penalty",
            "participants",
            "problems",
            "owner",
        ]
        read_only_fields = ["id", "owner", "participants", "problems"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
