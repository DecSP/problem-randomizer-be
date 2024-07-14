from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from problem_randomizer_be.contests.models import Contest
from problem_randomizer_be.contests.serializers import ContestSerializer
from problem_randomizer_be.utils.response import CustomResponse


class ContestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer

    def list(self, request, *args, **kwargs):
        contests = Contest.objects.filter(is_public=True)
        serializer = ContestSerializer(contests, many=True)
        return CustomResponse(status.HTTP_200_OK, "Contests retrieved successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        contest = self.get_object()
        serializer = ContestSerializer(contest)
        return CustomResponse(status.HTTP_200_OK, "Contest retrieved successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ContestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse(status.HTTP_201_CREATED, "Contest created successfully", serializer.data)
