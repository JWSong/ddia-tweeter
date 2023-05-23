from dataclasses import dataclass
from uuid import UUID


class Command:
    pass


@dataclass
class PostTweet(Command):
    user_id: UUID
    content: str
