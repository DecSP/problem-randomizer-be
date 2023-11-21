from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class CodeforcesProblems(APIView):
    def get(self, request):
        try:
            x = requests.get("https://codeforces.com/api/problemset.problems")
            problems = x.json()["result"]["problems"]
            return Response(problems)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
