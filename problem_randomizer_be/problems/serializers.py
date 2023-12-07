from rest_framework import serializers

from problem_randomizer_be.problems.models import Problem


class ProblemSerializer(serializers.ModelSerializer[Problem]):
    source_type = serializers.SerializerMethodField(source="get_source_type_display")

    def get_source_type(self, obj):
        return obj.get_source_type_display().lower()

    class Meta:
        model = Problem
        fields = ["source_type", "name", "contest_name", "url", "rating"]
