import asyncio

import httpx

from problem_randomizer_be.problems.models import Problem

from .html import CodeforcesProblemContentHTMLProcessor


class CodeforcesClient:
    content_html_processor = CodeforcesProblemContentHTMLProcessor()

    async def get_codeforces_problems(self, included_urls):
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

    def get_problem_content(self, url):
        html = httpx.get(url).text
        return self.content_html_processor.html_to_data(html)
