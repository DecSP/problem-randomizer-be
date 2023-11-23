from django.urls import path

from problem_randomizer_be.problems.views import UpdateProblemsViewSet

app_name = "problems"
urlpatterns = [
    path("update/<str:source_type>/", view=UpdateProblemsViewSet.as_view(), name="update"),
]
