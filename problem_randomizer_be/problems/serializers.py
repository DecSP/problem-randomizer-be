from rest_framework import serializers

from problem_randomizer_be.problems.models import Problem


class ProblemSerializer(serializers.ModelSerializer[Problem]):
    class Meta:
        model = Problem
        fields = ["source_type", "name", "contest_name", "url", "rating"]


class ProblemDetailSerializer(serializers.ModelSerializer[Problem]):
    class Meta:
        model = Problem
        fields = ["source_type", "name", "contest_name", "url", "rating", "content"]
