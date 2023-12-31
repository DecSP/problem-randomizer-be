from django.db import models


class Problem(models.Model):
    class SourceType(models.TextChoices):
        CODEFORCES = "codeforces", "Codeforces"
        ATCODER = "atcoder", "AtCoder"
        CSES = "cses", "CSES"

    source_type = models.CharField(max_length=50, choices=SourceType.choices, default=SourceType.CODEFORCES)
    name = models.CharField(max_length=256)
    contest_name = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=256)
    rating = models.IntegerField()

    class Meta:
        indexes = [models.Index(fields=["url"])]
