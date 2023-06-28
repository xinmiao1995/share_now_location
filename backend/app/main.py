from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

app = FastAPI()


class Coordinate(BaseModel):
    latitude: float = 0
    longitude: float = 0


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, client_id: int, coordinate: str):
        for connection in self.active_connections:
            await connection.send_json({
                "coordinate": coordinate,
                "message": f"user {client_id}'s location: {coordinate}"
            })


manager = ConnectionManager()


@app.get("/")
async def get():
    with open("viewer.html", "r", encoding='utf-8') as f:
        html = f.read()

    return HTMLResponse(html)


@app.post("/coordinate/")
async def create_location(coordinate: Coordinate):
    return coordinate


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            # await manager.send_personal_message(data, websocket)
            # await manager.broadcast_msg(f"user {client_id}'s location: {data}")
            # await manager.broadcast_loc(text)

            await manager.broadcast(client_id, text)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
