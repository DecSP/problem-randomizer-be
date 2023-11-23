from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from problem_randomizer_be.problems import constants
from problem_randomizer_be.problems.helpers import update_codeforces_problems
from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.serializers import ProblemSerializer


class UpdateProblemsViewSet(APIView):
    def get(self, request, source_type):
        if source_type == constants.CODEFORCES:
            try:
                update_codeforces_problems()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "specify problem source"}, status=status.HTTP_400_BAD_REQUEST)


class ProblemViewSet(ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
