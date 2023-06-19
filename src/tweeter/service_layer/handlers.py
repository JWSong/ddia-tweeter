from typing import Callable

from tweeter.domain import commands, events
from tweeter.service_layer import unit_of_work


def post_tweet(cmd: commands.PostTweet, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.users.get(cmd.user_id)
        user.post_tweet(content=cmd.content)
        uow.commit()


def put_in_cache_if_celeb(event: events.TweetPosted, uow: unit_of_work.AbstractUnitOfWork, cache: Callable):
    with uow:
        user = uow.users.get(event.user_id)
        if not user.is_celebrity:
            cache(tweet_id=event.tweet_id, user_id=user.id, content=event.content, create_dt=event.create_dt)


def became_celebrity(event: events.UserPromoted, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.users.get(event.user_id)
        user.become_celebrity()
        uow.commit()


def follow_user(
    cmd: commands.FollowUser, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        user = uow.users.get(cmd.user_id)
        user_to_follow = uow.users.get(cmd.following_id)
        user.follow(user_to_follow)
        uow.commit()


EVENT_HANDLERS = {
    events.TweetPosted: put_in_cache_if_celeb,
    events.UserPromoted: became_celebrity,
}

COMMAND_HANDLERS = {
    commands.PostTweet: post_tweet,
    commands.FollowUser: follow_user,
}
