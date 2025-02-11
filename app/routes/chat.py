from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utile.chat_manage import manager
import json
import random


route = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@route.get("/", response_class=HTMLResponse)
async def get(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})


@route.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    client_id = random.randint(1000, 9999)
    await manager.connect(websocket, client_id)

    # Send client ID to the connected user
    await manager.send_personal_message(
        json.dumps({"type": "init", "client_id": client_id}), websocket
    )

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
                message = data.get("message", "")
            except json.JSONDecodeError:
                message = raw_data

            response = {
                "type": "message",
                "message": message,
                "client_id": client_id,
                "img_like": f"https://api.dicebear.com/7.x/personas/svg?seed={client_id}",
            }

            await manager.broadcast(json.dumps(response), exclude=websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            json.dumps(
                {"type": "message", "message": f"Client #{client_id} left the chat"}
            )
        )
        await manager.broadcast_user_count()
