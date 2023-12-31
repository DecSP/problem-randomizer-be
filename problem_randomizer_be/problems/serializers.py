from rest_framework import serializers

from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.services import services


class ProblemSerializer(serializers.ModelSerializer[Problem]):
    class Meta:
        model = Problem
        fields = ["id", "source_type", "name", "contest_name", "url", "rating"]


class ProblemDetailSerializer(serializers.ModelSerializer[Problem]):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ["id", "source_type", "name", "contest_name", "url", "rating", "content"]

    def get_content(self, obj):
        if obj.source_type in [Problem.SourceType.ATCODER, Problem.SourceType.CODEFORCES]:
            return services[obj.source_type].get_problem_content(obj.url)
        return "NOT IMPLEMENTED"
