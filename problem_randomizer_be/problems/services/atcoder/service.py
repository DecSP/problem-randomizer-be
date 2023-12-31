from asgiref.sync import async_to_sync

from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.services.interfaces import ProblemSourceService

from .client import AtcoderClient


class AtcoderService(ProblemSourceService):
    client = AtcoderClient()

    def update_problems(self):
        included_urls = set(
            Problem.objects.filter(source_type=Problem.SourceType.ATCODER).values_list("url", flat=True)
        )
        problems = async_to_sync(self.client.get_atcoder_problems)(included_urls)
        if problems:
            Problem.objects.bulk_create(problems)
        return len(problems)

    def get_problem_content(self, problem):
        return self.client.get_atcoder_content(problem)
