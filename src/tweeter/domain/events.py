import datetime
from dataclasses import dataclass
from uuid import UUID


class Event:
    pass


@dataclass
class UserPromoted(Event):
    user_id: UUID


@dataclass
class TweetPosted(Event):
    tweet_id: UUID
    user_id: UUID
    content: str
    create_dt: datetime.datetime


@dataclass
class UserFollowed(Event):
    user_id: UUID
    following_id: UUID
