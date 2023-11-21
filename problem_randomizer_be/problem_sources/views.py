import asyncio

import httpx
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


async def get_codeforces_problems():
    urls = ["https://codeforces.com/api/problemset.problems", "https://codeforces.com/api/contest.list"]
    client = httpx.AsyncClient()
    fetches = [client.get(url) for url in urls]
    problem_data, contest_data = await asyncio.gather(*fetches)
    await client.aclose()

    problems = problem_data.json()["result"]["problems"]
    contests = contest_data.json()["result"]
    contest_dict = {contest["id"]: contest for contest in contests}

    return [
        {
            "name": problem["name"],
            "contestName": contest_dict[problem["contestId"]]["name"],
            "url": f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}",
            "rating": problem["rating"],
        }
        for problem in problems
        if "rating" in problem
    ]


class CodeforcesProblems(APIView):
    def get(self, request):
        try:
            data = async_to_sync(get_codeforces_problems)()
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
