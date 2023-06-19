import datetime
import uuid
from uuid import UUID

from tweeter.domain import events


class User:
    def __init__(
        self,
        ref: UUID,
        name: str,
        timeline=None,
        is_celebrity: bool = False,
        version_number: int = 0,
    ):
        if timeline is None:
            timeline = set()
        self.id = ref
        self.name = name
        self.timeline: set["Tweet"] = timeline
        self.is_celebrity: bool = is_celebrity
        self.followers: set["User"] = set()
        self.events = []
        self.version_number = version_number

    def post_tweet(self, content: str):
        tweet = Tweet(
            ref=uuid.uuid4(),
            user=self,
            content=content,
            create_dt=datetime.datetime.now(),
        )
        self.timeline.add(tweet)
        self.events.append(
            events.TweetPosted(tweet.id, self.id, tweet.content, tweet.create_dt)
        )

    def become_celebrity(self):
        self.is_celebrity = True

    def follow(self, user: "User"):
        self.followers.add(user)
        self.events.append(
            events.UserFollowed(
                user_id=self.id,
                following_id=user.id,
            )
        )


class Tweet:
    def __init__(
        self,
        ref: UUID,
        user: "User",
        create_dt: datetime.datetime,
        content: str,
    ):
        self.id = ref
        self.user = user
        self.content = content
        self.create_dt = create_dt
