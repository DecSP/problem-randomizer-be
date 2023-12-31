from typing import Any

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.serializers import ProblemDetailSerializer, ProblemSerializer
from problem_randomizer_be.problems.services import services


class UpdateProblemsViewSet(APIView):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def get(self, request, source_type):
        if source_type in services:
            update_func = services[source_type].update_problems
            try:
                num_updated = update_func()
                return Response({"detail": f"update {num_updated} new problems"}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "specify problem source"}, status=status.HTTP_400_BAD_REQUEST)


class ProblemViewSet(ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @action(detail=False, url_path=r"by-source/(?P<source_type>\w+)")
    def by_source(self, request, source_type):
        problems = self.queryset.filter(source_type=source_type)
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        problem = self.get_object()
        serializer = ProblemDetailSerializer(problem)
        return Response(serializer.data)
