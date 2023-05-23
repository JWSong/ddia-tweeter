import logging

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    UUID,
    event,
)

from sqlalchemy.orm import registry, relationship

from tweeter.domain import model

logger = logging.getLogger(__name__)

mapper_registry = registry()

user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("name", String(50)),
)

tweet_table = Table(
    "tweet",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("content", String(255)),
    Column("create_dt", DateTime(timezone=True)),
    Column("user_id", ForeignKey("users.id")),
)


def start_mappers():
    logger.info("Staring mappers")
    mapper_registry.map_imperatively(
        model.User,
        user_table,
        properties={
            "timeline": relationship(
                model.Tweet,
                backref="user",
                order_by=tweet_table.c.create_dt.desc(),
                collection_class=set,
            ),
        },
    )
    mapper_registry.map_imperatively(
        model.Tweet,
        tweet_table,
        properties={"user": relationship(model.User, backref="tweet")},
    )


@event.listens_for(model.Tweet, "load")
def receive_load(user, _):
    user.events = []
