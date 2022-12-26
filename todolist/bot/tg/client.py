import requests
from requests import Response

from .dc import (
    GetUpdatesResponse,
    SendMessageResponse,
    GetUpdatesResponseSchema,
    SendMessageResponseSchema
)


class TgClient:
    def __init__(self, token) -> None:
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url: str = self.get_url('getUpdates')
        resp: Response = requests.get(
            url,
            params={
                'offset': offset,
                'timeout': timeout
            }
        )
        return GetUpdatesResponseSchema.load(resp.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url: str = self.get_url('sendMessage')
        resp: Response = requests.post(
            url,
            json={
                'chat_id': chat_id,
                'text': text
            }
        )
        return SendMessageResponseSchema.load(resp.json())
