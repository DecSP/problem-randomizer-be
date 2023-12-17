import asyncio
from urllib.parse import urljoin

import httpx
import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup as bs

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
            source_type=Problem.SourceType.CODEFORCES,
        )
        for problem in problems
        if "rating" in problem
    ]
    return problems


def update_codeforces_problems():
    problems = async_to_sync(get_codeforces_problems)()
    if problems:
        Problem.objects.filter(source_type=Problem.SourceType.CODEFORCES).delete()
        Problem.objects.bulk_create(problems)


async def get_atcoder_problems():
    urls = [
        "https://kenkoooo.com/atcoder/resources/problems.json",
        "https://kenkoooo.com/atcoder/resources/problem-models.json",
        "https://kenkoooo.com/atcoder/resources/contests.json",
    ]
    client = httpx.AsyncClient()
    fetches = [client.get(url) for url in urls]
    problem_data, problem_model_data, contest_data = [data.json() for data in await asyncio.gather(*fetches)]
    await client.aclose()
    contest_dict = {contest["id"]: contest for contest in contest_data}
    prob_with_models = filter(
        lambda prob: prob["id"] in problem_model_data and "difficulty" in problem_model_data[prob["id"]], problem_data
    )
    problems = [
        Problem(
            name=problem["name"],
            contest_name=contest_dict[problem["contest_id"]]["title"],
            url=f"https://atcoder.jp/contests/{problem['contest_id']}/tasks/{problem['id']}",
            rating=problem_model_data[problem["id"]]["difficulty"],
            source_type=Problem.SourceType.ATCODER,
        )
        for problem in prob_with_models
    ]
    return problems


def update_atcoder_problems():
    problems = async_to_sync(get_atcoder_problems)()
    if problems:
        Problem.objects.filter(source_type=Problem.SourceType.ATCODER).delete()
        Problem.objects.bulk_create(problems)


def get_cses_problems():
    url = "https://cses.fi/problemset"
    html = requests.get(url).text
    soup = bs(html, "html.parser")
    problems = []
    for h2_tag in soup.find_all("h2")[1:]:
        next_sibling = h2_tag.find_next_sibling()
        if next_sibling and next_sibling.name == "ul":
            for link in next_sibling.find_all("a"):
                path = link.get("href")
                if path and path.startswith("/problemset/task"):
                    problem_url = urljoin(url, path)
                    problems.append(
                        Problem(
                            name=link.text,
                            contest_name=h2_tag.text,
                            url=problem_url,
                            rating=1000,
                            source_type=Problem.SourceType.CSES,
                        )
                    )
    return problems


def update_cses_problems():
    problems = get_cses_problems()
    if problems:
        Problem.objects.filter(source_type=Problem.SourceType.CSES).delete()
        Problem.objects.bulk_create(problems)
