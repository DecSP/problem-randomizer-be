from problem_randomizer_be.problems.models import Problem

from .atcoder.service import AtcoderService
from .codeforces.service import CodeforcesService
from .cses.service import CsesService

services = {
    Problem.SourceType.ATCODER: AtcoderService(),
    Problem.SourceType.CODEFORCES: CodeforcesService(),
    Problem.SourceType.CSES: CsesService(),
}
