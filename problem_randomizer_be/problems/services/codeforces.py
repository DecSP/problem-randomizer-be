import asyncio

import httpx
from asgiref.sync import async_to_sync

from problem_randomizer_be.problems.models import Problem


async def get_codeforces_problems(included_urls):
    urls = ["https://codeforces.com/api/problemset.problems", "https://codeforces.com/api/contest.list"]
    client = httpx.AsyncClient()
    fetches = [client.get(url) for url in urls]
    problem_data, contest_data = await asyncio.gather(*fetches)
    await client.aclose()

    problems = problem_data.json()["result"]["problems"]
    contests = contest_data.json()["result"]
    contest_dict = {contest["id"]: contest for contest in contests}

    problems = [
        Problem(
            name=problem["name"],
            contest_name=contest_dict[problem["contestId"]]["name"],
            url=url,
            rating=problem["rating"],
            source_type=Problem.SourceType.CODEFORCES,
        )
        for problem in problems
        if "rating" in problem
        and (url := f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}")
        not in included_urls
    ]

    return problems


def update_codeforces_problems():
    included_urls = set(
        Problem.objects.filter(source_type=Problem.SourceType.CODEFORCES).values_list("url", flat=True)
    )

    problems = async_to_sync(get_codeforces_problems)(included_urls)
    if problems:
        Problem.objects.filter(source_type=Problem.SourceType.CODEFORCES).delete()
        Problem.objects.bulk_create(problems)
    return len(problems)
