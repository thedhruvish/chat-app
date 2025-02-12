import urllib.parse
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.sqllit_db import Connection
from app.schemas.user import UserData
from typing import cast
import os
import requests


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
SCOPES = [
	"https://www.googleapis.com/auth/userinfo.profile",
	"https://www.googleapis.com/auth/userinfo.email",
]

route = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@route.get("/", response_class=HTMLResponse)
def home(req: Request):
	if req.session.get("user"):
		return "<a href='/auth/logout'>Logout</a>"
	return '<a href="/auth/login">Login with Google</a>'


@route.get("/logout", response_class=RedirectResponse)
def logout(req: Request):
	req.session.clear()
	return RedirectResponse("/")


@route.get("/login", response_class=RedirectResponse)
def login():
	params = {
		"client_id": GOOGLE_CLIENT_ID,
		"response_type": "code",
		"scope": " ".join(SCOPES),
		"redirect_uri": REDIRECT_URI,
		"access_type": "offline",
		"prompt": "consent",
	}
	url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
	return RedirectResponse(url)


@route.get("/callback", response_class=RedirectResponse)
def auth_callback(request: Request, code: str):
	data = {
		"code": code,
		"client_id": GOOGLE_CLIENT_ID,
		"client_secret": GOOGLE_CLIENT_SECRET,
		"redirect_uri": REDIRECT_URI,
		"grant_type": "authorization_code",
	}

	token_resp = requests.post(TOKEN_URL, data=data)
	token_json = token_resp.json()
	access_token = token_json.get("access_token")

	headers = {"Authorization": f"Bearer {access_token}"}
	user_resp = requests.get(USERINFO_URL, headers=headers)
	user_info = user_resp.json()
	user_info = UserData(**user_info).model_dump()
	print(user_info)

	db = cast(Connection, request.app.state.db)  # noqa: F821
	db.cursor.execute(
		"""INSERT OR IGNORE INTO users (g_id, name, email, given_name, picture) VALUES (?, ?, ?, ?, ?) ON CONFLICT(email) DO UPDATE SET
        g_id=excluded.g_id,
        name=excluded.name,
        given_name=excluded.given_name,
        picture=excluded.picture
    RETURNING  id """,
		(
			str(user_info["id"]),
			user_info["name"],
			user_info["email"],
			user_info["given_name"],
			user_info["picture"],
		),
	)

	user_row = db.cursor.fetchone()
	user_info["id"] = user_row[0]
	user_info["g_id"] = str(user_info["id"])
	db.connection.commit()
	print(user_info)

	request.session["user"] = user_info
	return RedirectResponse("/")


def get_current_user(req: Request):
	user = req.session.get("user")
	if not user:
		return RedirectResponse("/auth/login")
	return user
