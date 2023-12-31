from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.services.interfaces import ProblemSourceService

from .client import CsesClient


class CsesService(ProblemSourceService):
    client = CsesClient()

    def update_problems(self):
        problems = self.client.get_cses_problems()
        if problems:
            Problem.objects.bulk_create(problems)
        return len(problems)

    def get_problem_content(self, problem_url):
        return self.client.get_problem_content(problem_url)
