import abc


class ProblemSourceService(abc.ABC):
    @abc.abstractmethod
    def update_problems(self):
        pass

    @abc.abstractmethod
    def get_problem_content(self, problem):
        pass
