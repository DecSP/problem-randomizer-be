import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from problem_randomizer_be.problems.models import Problem
from problem_randomizer_be.problems.services import services


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)

        problem_url = await self.get_problem_url(message["problem_id"])
        if not problem_url:
            await self.send(text_data=json.dumps({"message": "problem not exists"}))
            return
        if message["source_type"] == "atcoder":
            code = message.get("code", "")
            try:
                async for message in services[message["source_type"]].submit_problem(problem_url, code):
                    await self.send(text_data=json.dumps({"message": message}))
            except Exception as e:
                await self.send(text_data=json.dumps({"message": f"An error occurred {e}"}))
        else:
            await self.send(text_data=json.dumps({"message": "NOT IMPLEMENTED"}))

    @database_sync_to_async
    def get_problem_url(self, problem_id):
        problem = Problem.objects.filter(pk=problem_id).first()
        if problem:
            return problem.url
        return None
