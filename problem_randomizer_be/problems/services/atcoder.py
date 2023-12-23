import asyncio

import httpx
import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup as bs

from problem_randomizer_be.problems.models import Problem


async def get_atcoder_problems(included_urls):
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

    def get_content(url):
        html = requests.get(url).text
        soup = bs(html, "html.parser")
        span_with_lang_en = soup.find("span", {"class": "lang-en"})
        if not span_with_lang_en:
            return ""
        first_p_tag = span_with_lang_en.find("p")
        if first_p_tag and first_p_tag.text.startswith("Score"):
            first_p_tag.extract()
        return str(span_with_lang_en)

    problems = [
        Problem(
            name=problem["name"],
            contest_name=contest_dict[problem["contest_id"]]["title"],
            url=url,
            rating=problem_model_data[problem["id"]]["difficulty"],
            source_type=Problem.SourceType.ATCODER,
            content=get_content(f"https://atcoder.jp/contests/{problem['contest_id']}/tasks/{problem['id']}"),
        )
        for problem in prob_with_models
        if (url := f"https://atcoder.jp/contests/{problem['contest_id']}/tasks/{problem['id']}") not in included_urls
    ]

    return problems


def update_atcoder_problems():
    included_urls = set(Problem.objects.filter(source_type=Problem.SourceType.ATCODER).values_list("url", flat=True))
    problems = async_to_sync(get_atcoder_problems)(included_urls)
    if problems:
        Problem.objects.filter(source_type=Problem.SourceType.ATCODER).delete()
        Problem.objects.bulk_create(problems)
    return len(problems)
