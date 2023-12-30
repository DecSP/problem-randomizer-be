import asyncio
from urllib.parse import unquote

import httpx
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup as bs
from django.conf import settings

from problem_randomizer_be.problems.models import Problem

from .atcoder_bs import html_to_dict


class AtcoderService:
    async def get_atcoder_problems(self, included_urls):
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
            lambda prob: prob["id"] in problem_model_data and "difficulty" in problem_model_data[prob["id"]],
            problem_data,
        )

        problems = [
            Problem(
                name=problem["name"],
                contest_name=contest_dict[problem["contest_id"]]["title"],
                url=url,
                rating=problem_model_data[problem["id"]]["difficulty"],
                source_type=Problem.SourceType.ATCODER,
            )
            for problem in prob_with_models
            if (url := f"https://atcoder.jp/contests/{problem['contest_id']}/tasks/{problem['id']}")
            not in included_urls
        ]

        return problems

    def get_atcoder_content(self, url):
        html = httpx.get(url).text
        return html_to_dict(html)

    def update_atcoder_problems(self):
        included_urls = set(
            Problem.objects.filter(source_type=Problem.SourceType.ATCODER).values_list("url", flat=True)
        )
        problems = async_to_sync(self.get_atcoder_problems)(included_urls)
        if problems:
            Problem.objects.bulk_create(problems)
        return len(problems)

    def __get_csrf_token(self, resp):
        ss_cookies = unquote(resp.cookies.get("REVEL_SESSION"))
        csrf_token_index = ss_cookies.index("csrf_token:") + len("csrf_token:")
        csrf_token = ss_cookies[csrf_token_index:].split("\x00")[0]
        return csrf_token

    async def login(self, session):
        resp = await session.get("https://atcoder.jp/login?continue=https://atcoder.jp/")
        login_data = {
            "username": settings.ATCODER_USERNAME,
            "password": settings.ATCODER_PASSWORD,
            "csrf_token": self.__get_csrf_token(resp),
        }
        resp = await session.post("https://atcoder.jp/login?continue=https://atcoder.jp/", data=login_data)
        assert resp.status_code != 403
        return self.__get_csrf_token(resp)

    async def submit_problem(self, url, code):
        task_name = url.split("/")[-1]
        contest_id = task_name.split("_")[0]
        async with httpx.AsyncClient() as session:
            csrf_token = await self.login(session)
            post_data = {
                "data.LanguageId": "5078",  # only support python for now
                "data.TaskScreenName": task_name,
                "sourceCode": code,
                "csrf_token": csrf_token,
            }
            await session.post(f"https://atcoder.jp/contests/{contest_id}/submit", data=post_data)
            resp = await session.get(f"https://atcoder.jp/contests/{contest_id}/submissions/me")
            submission_link = self.__get_submission_link(resp)
            assert submission_link
            sub_id = submission_link.split("/")[-1]

            yield "Judging"
            score = 0
            while True:
                await asyncio.sleep(1)
                resp = await self.__get_submission_status(session, sub_id, contest_id)
                x = resp.json()
                if "Interval" not in x:
                    score = int(x["Result"][sub_id]["Score"])
                    break
            yield "Accepted" if score > 0 else "Failed"

    def __get_submission_link(self, resp):
        soup = bs(resp.content, "html.parser")

        # Find the first link within the table
        tbody_element = soup.find("tbody")

        if tbody_element:
            tr_element = tbody_element.find("tr")
            if tr_element:
                # Find the first link within the tr
                link_element = tr_element.find("a", string="Detail", href=True)
                if link_element:
                    link = link_element["href"]
                    return link
        return None

    async def __get_submission_status(self, session, submission_id, contest_id):
        url = f"https://atcoder.jp/contests/{contest_id}/submissions/me/status/json?reload=true&sids[]={submission_id}"
        return await session.get(url)
