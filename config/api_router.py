from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from problem_randomizer_be.problems.views import ProblemViewSet
from problem_randomizer_be.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("problems", ProblemViewSet, basename="problems")

app_name = "api"
urlpatterns = router.urls


urlpatterns += [
    path("problems/", include("problem_randomizer_be.problems.urls")),
    path("users/", include("problem_randomizer_be.users.api.urls")),
]
