from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from problem_randomizer_be.utils.response import CustomResponse

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = "username"
    queryset = User.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return CustomResponse(status_code=status.HTTP_200_OK, message="", data=serializer.data)

    @action(detail=False, permission_classes=[])
    def count(self, request):
        user_count = User.objects.count()
        return CustomResponse(status.HTTP_200_OK, "User count retrieved successfully", user_count)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return CustomResponse(
                status.HTTP_200_OK,
                "Login successfully",
                {"token": token.key, "user": serializer.data},
            )
        return CustomResponse(status.HTTP_401_UNAUTHORIZED, "Invalid credentials", False)


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return CustomResponse(status.HTTP_201_CREATED, "Created user successfully", True)
