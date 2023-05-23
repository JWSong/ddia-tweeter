from uuid import UUID

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from tweeter import views
from tweeter.domain import commands
from tweeter.entrypoints.deps import get_message_bus
from tweeter.service_layer.messagebus import MessageBus

app = FastAPI()


class TimelineOut(BaseModel):
    id: UUID
    content: str
    create_dt: str


class TimelineListOut(BaseModel):
    timelines: list[TimelineOut]
    user_id: UUID


@app.get("/users/{user_id}/timeline")
def get_timeline(
    user_id: UUID, bus: MessageBus = Depends(get_message_bus)
) -> TimelineListOut:
    timelines = views.timelines(user_id, bus.uow)
    return TimelineListOut(timelines=timelines, user_id=user_id)


@app.post("/users/{user_id}/tweets")
def post_tweet(user_id: UUID, bus: MessageBus = Depends(get_message_bus)):
    try:
        cmd = commands.PostTweet(user_id=user_id, content="Hello, world!")
        bus.handle(message=cmd)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    return JSONResponse(status_code=201, content={"message": "Tweet posted"})
