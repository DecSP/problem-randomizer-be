import asyncio

import httpx
from asgiref.sync import async_to_sync

from problem_randomizer_be.problems import constants
from problem_randomizer_be.problems.models import Problem


async def get_codeforces_problems():
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
            url=f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}",
            rating=problem["rating"],
            source_type="cf",
        )
        for problem in problems
        if "rating" in problem
    ]
    return problems


def update_codeforces_problems():
    problems = async_to_sync(get_codeforces_problems)()
    if problems:
        Problem.objects.filter(source_type=constants.CODEFORCES).delete()
        Problem.objects.bulk_create(problems)
