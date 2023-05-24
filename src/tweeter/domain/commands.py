from dataclasses import dataclass
from uuid import UUID


class Command:
    pass


@dataclass
class PostTweet(Command):
    user_id: UUID
    content: str


@dataclass
class FollowUser(Command):
    user_id: UUID
    following_id: UUID
