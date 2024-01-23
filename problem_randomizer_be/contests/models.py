from django.db import models
from django_extensions.db.models import TimeStampedModel


class Contest(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    start_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    penalty = models.IntegerField(default=0)
    participants = models.ManyToManyField("users.User", related_name="contests")
    problems = models.ManyToManyField("problems.Problem", related_name="contests")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="owned_contests")


class ContestProblemStatus(TimeStampedModel):
    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE, related_name="problem_statuses")
    problem = models.ForeignKey("problems.Problem", on_delete=models.CASCADE, related_name="contest_statuses")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="problem_statuses")
    is_solved = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)
    last_submission_time = models.DateTimeField(null=True, blank=True)
