from collections import defaultdict

from fastapi import WebSocket
from redis import Redis

from chat_service.core.config import Settings, SettingsDep


class ConnectionManager:
    def __init__(self, settings: SettingsDep):
        self.active_connections: dict[int, dict[int, WebSocket]] = defaultdict(dict)
        self.redis: Redis = Redis.from_url(str(settings.redis_settings.redis_dsn))
        self.settings: Settings = settings

    async def connect(self, ws: WebSocket, room_id: int, user_id: int) -> None:
        await ws.accept()
        self.active_connections[room_id][user_id] = ws

    async def disconnect(self, room_id: int, user_id: int) -> None:
        if self.active_connections[room_id][user_id] != {}:
            del self.active_connections[room_id][user_id]

    async def broadcast(self, message: str, room_id: int, sender_id: int) -> None:
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                msg = {"text": message, "is_self": user_id == sender_id}
                await connection.send_json(msg)


def get_con_manager(settings: SettingsDep) -> ConnectionManager:
    return ConnectionManager(settings)
