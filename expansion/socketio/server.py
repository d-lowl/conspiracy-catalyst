import dataclasses
import os
from typing import Any

from dataclasses_json import DataClassJsonMixin
from loguru import logger

import socketio
from sanic import Sanic
from sanic_cors import CORS

from expansion.game import Game

static_path = os.path.join(os.path.dirname(__file__), "static")

games: dict[str, Game] = {}

sio = socketio.AsyncServer(async_mode="sanic", cors_allowed_origins="*")

app = Sanic(name="cblit")
app.static("/", os.path.join(static_path, "index.html"), name="game")
app.static("/static/", static_path, name="statics")
CORS(app, resources={r"*": {"origins": "*"}})
sio.attach(app)


@sio.event
async def connect(sid: str, environ: Any, auth: Any) -> None:
    """Connect event handler.

    Args:
        sid (str): session ID
        environ (Any): unused
        auth (Any): unused
    """
    logger.info(f"Connected: {sid}")
    games[sid] = Game()


@sio.event
def disconnect(sid: str) -> None:
    """Disconnect event handler.

    Args:
        sid (str): session ID
    """
    logger.info(f"Disconnected: {sid}")
    del games[sid]


@dataclasses.dataclass
class SayPayload(DataClassJsonMixin):
    """Say payload."""
    message_id: int
    message: str


@sio.event
async def say(sid: str, data: str) -> None:
    """Say event handler.

    Args:
        sid (str): session ID
        data (str): raw event data
    """
    try:
        payload = SayPayload.from_json(data)
        turn = games[sid].make_turn(payload.message_id, payload.message)
        await sio.emit(
            "turn",
            turn.json(),
            sid
        )
    except Exception as e:
        await sio.emit(
            "error",
            str(e),
            sid
        )


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app.run(host=host, port=port)
