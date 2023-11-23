from django.db import models

from problem_randomizer_be.problems import constants

SOURCE_TYPE_CHOICES = ((constants.CODEFORCES, "Codeforces"), (constants.ATCODER, "AtCoder"))


class Problem(models.Model):
    source_type = models.CharField(max_length=2, choices=SOURCE_TYPE_CHOICES)
    name = models.CharField(max_length=256)
    contest_name = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=256)
    rating = models.IntegerField()
