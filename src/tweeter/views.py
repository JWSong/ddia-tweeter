from uuid import UUID

from tweeter.service_layer import unit_of_work


def timelines(user_id: UUID, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        celeb_tweets = uow.session.execute(
            """
            SELECT t.id, t.content, t.create_dt, t.user_id, u.id, u.name
            FROM tweet t
            JOIN users u ON t.user_id = u.id
            WHERE u.id = :user_id and users.is_celebrity
            ORDER BY t.create_dt DESC
            LIMIT 30
            """,
            dict(user_id=user_id),
        )

    return [dict(t) for t in tweets]
