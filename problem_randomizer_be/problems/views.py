from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from problem_randomizer_be.problems import constants, helpers
from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.serializers import ProblemSerializer


class UpdateProblemsViewSet(APIView):
    UPDATE_FUNCTION_MAP = {
        constants.CODEFORCES: helpers.update_codeforces_problems,
        constants.ATCODER: helpers.update_atcoder_problems,
        constants.CSES: helpers.update_cses_problems,
    }

    def get(self, request, source_type):
        if source_type in self.UPDATE_FUNCTION_MAP:
            update_func = self.UPDATE_FUNCTION_MAP[source_type]
            try:
                update_func()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "specify problem source"}, status=status.HTTP_400_BAD_REQUEST)


class ProblemViewSet(ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @action(detail=False)
    def codeforces(self, request):
        cf = self.queryset.filter(source_type=constants.CODEFORCES)
        serializer = ProblemSerializer(cf, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def atcoder(self, request):
        ac = self.queryset.filter(source_type=constants.ATCODER)
        serializer = ProblemSerializer(ac, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def cses(self, request):
        cses = self.queryset.filter(source_type=constants.CSES)
        serializer = ProblemSerializer(cses, many=True)
        return Response(serializer.data)
