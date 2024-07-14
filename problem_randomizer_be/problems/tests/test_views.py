from django.test import TestCase
from django.urls import reverse

from problem_randomizer_be.problems.models import Problem


class TestProblemViewSet(TestCase):
    def setUp(self) -> None:
        self.problems = [
            Problem(
                name="prob1",
                contest_name="con1",
                url="www.prob1.com",
                rating=100,
                source_type=Problem.SourceType.CODEFORCES,
            )
        ]
        Problem.objects.bulk_create(self.problems)

    def tearDown(self):
        Problem.objects.filter(id__in=[problem.id for problem in self.problems]).delete()

    def test_codeforces_problems(self):
        url = reverse("api:problems-by-source", kwargs={"source_type": "codeforces"})
        response = self.client.get(url)
        self.assertCountEqual(
            response.json()[0],
            {
                "id": self.problems[0].id,
                "source_type": "codeforces",
                "name": "prob1",
                "contest_name": "con1",
                "rating": 100,
                "url": "www.prob1.com",
            },
        )
        assert len(response.json()) == 1
