from dataclasses import field
from typing import (
    List,
    Optional
)

from marshmallow_dataclass import (
    dataclass,
    class_schema
)
from marshmallow import EXCLUDE


class BaseMeta:
    class Meta:
        unknown = EXCLUDE

@dataclass
class MessageFrom(BaseMeta):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str


@dataclass
class Chat(BaseMeta):
    id: int
    type: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    title: Optional[str]


@dataclass
class Message(BaseMeta):
    message_id: int
    from_: MessageFrom = field(
        metadata={
            'data_key': 'from'
        }
    )
    chat: Chat
    text: Optional[str]


@dataclass
class UpdateObj:
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message


GetUpdatesResponseSchema = class_schema(
    GetUpdatesResponse
)()
SendMessageResponseSchema = class_schema(
    SendMessageResponse
)()
