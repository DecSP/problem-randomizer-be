from django.urls import path

from problem_randomizer_be.problem_sources.views import CodeforcesProblems

app_name = "problem_sources"
urlpatterns = [
    path("codeforces/", view=CodeforcesProblems.as_view(), name="codeforces_problems"),
]
