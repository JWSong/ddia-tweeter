import uuid

from tweeter.domain import commands, events
from tweeter.domain.model import User
from tweeter.service_layer.messagebus import MessageBus


def test_follow():
    user1_id = uuid.uuid4()
    user1 = User(
        ref=user1_id,
        name="user1",
    )
    user2_id = uuid.uuid4()
    user2 = User(
        ref=user2_id,
        name="user2",
    )
    user1.follow(user2)
    assert user1.followers == {user2}

    user2.follow(user1)
    assert user2.followers == {user1}


def test_follow_cmd(message_bus: MessageBus):
    user1_id = uuid.uuid4()
    user1 = User(
        ref=user1_id,
        name="user1",
    )
    user2_id = uuid.uuid4()
    user2 = User(
        ref=user2_id,
        name="user2",
    )

    cmd = commands.FollowUser(user_id=user1_id, following_id=user2_id)
    message_bus.handle(message=cmd)
    assert user1.followers == {user2}
    assert user2.followers == set()

    cmd = commands.FollowUser(user_id=user2_id, following_id=user1_id)
    message_bus.handle(message=cmd)
    assert user1.followers == {user2}
    assert user2.followers == {user1}


def test_become_celebrity():
    user1_id = uuid.uuid4()
    user1 = User(
        ref=user1_id,
        name="user1",
    )
    assert user1.is_celebrity is False
    user1.become_celebrity()
    assert user1.is_celebrity is True


def test_become_celebrity_event(message_bus: MessageBus):
    user1_id = uuid.uuid4()
    user1 = User(
        ref=user1_id,
        name="user1",
    )
    assert user1.is_celebrity is False
    cmd = events.UserPromoted(user_id=user1_id)
    message_bus.handle(message=cmd)
    assert user1.is_celebrity is True
