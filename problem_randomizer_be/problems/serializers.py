from rest_framework import serializers

from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.services.atcoder import AtcoderService


class ProblemSerializer(serializers.ModelSerializer[Problem]):
    class Meta:
        model = Problem
        fields = ["id", "source_type", "name", "contest_name", "url", "rating"]


class ProblemDetailSerializer(serializers.ModelSerializer[Problem]):
    atcoder_service = AtcoderService()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ["id", "source_type", "name", "contest_name", "url", "rating", "content"]

    def get_content(self, obj):
        if obj.source_type == Problem.SourceType.ATCODER:
            return self.atcoder_service.get_atcoder_content(obj.url)
        return "NOT IMPLEMENTED"
