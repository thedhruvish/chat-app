from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utile.chat_manage import manager
from app.db.sqllit_db import Connection
import json
import random
from typing import cast

route = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@route.get("/", response_class=HTMLResponse)
async def get(req: Request):
	if req.session.get("user"):
		user = req.session.get("user")
		return templates.TemplateResponse(
			"index.html",
			context={
				"request": req,
				"user": user,
			},
		)
	return templates.TemplateResponse(
		"index.html", context={"request": req, "user": None}
	)


@route.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
	session = websocket.session
	user = session.get("user") if session else None

	client_id = user["id"] if user else random.randint(10000, 99999)
	print(client_id)
	await manager.connect(websocket, client_id)

	# Send client ID to the connected user
	await manager.send_personal_message(
		json.dumps({"type": "init", "client_id": client_id}), websocket
	)

	try:
		img_like = user.get("picture", "") if user else ""
		user_email = user.get("email", "") if user else ""
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
				"img_like": img_like,
				"email": user_email,
			}
			if user_email:
				db = cast(Connection, websocket.app.state.db)
				db.cursor.execute(
					"INSERT INTO messages (message, user_id) VALUES (?, ?)",
					(message, client_id),
				)
				db.connection.commit()
			await manager.broadcast(json.dumps(response), exclude=websocket)

	except WebSocketDisconnect:
		manager.disconnect(websocket)
		await manager.broadcast(
			json.dumps(
				{"type": "info", "message": f"Client #{client_id} left the chat"}
			)
		)
		await manager.broadcast_user_count()
