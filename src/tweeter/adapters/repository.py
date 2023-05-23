import abc
from typing import Set
from uuid import UUID

from tweeter.adapters import orm
from tweeter.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set[model.User] = set()

    def add(self, user: model.User):
        self._add(user)
        self.seen.add(user)

    def get(self, user_id: UUID) -> model.User | None:
        user = self._get(user_id)
        if user:
            self.seen.add(user)
        return user

    def get_by_tweet(self, tweet_id: UUID) -> list[model.User]:
        tweets = self._get_by_tweet(tweet_id)
        if tweets:
            self.seen.union(tweets)
        return tweets

    @abc.abstractmethod
    def _add(self, tweet: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_id: UUID) -> model.User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_tweet(self, tweet_id: UUID) -> model.User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, user: model.User):
        self.session.add(user)

    def _get(self, user_id: UUID) -> model.User | None:
        return self.session.get(model.User, user_id)

    def _get_by_tweet(self, tweet_id: UUID) -> model.User:
        return (
            self.session.query(model.User)
            .join(model.Tweet)
            .filter(
                orm.tweet_table.c.id == tweet_id,
            )
            .first()
        )
