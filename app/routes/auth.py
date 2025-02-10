import urllib.parse
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
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


@route.get("/", response_class=HTMLResponse)
def home(req: Request):
    if req.session.get("user"):
        return "<a href='/auth/logout'>Logout</a>"
    return '<a href="/auth/login">Login with Google</a>'


@route.get("/login")
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


@route.get("/callback")
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

    request.session["user"] = user_info
    return HTMLResponse(
        content=f"<h1>Hello {user_info['name']}</h1><p>Email: {user_info['email']}</p>"
    )


def get_current_user(req: Request):
    user = req.session.get("user")
    if not user:
        return RedirectResponse("/auth/login")
    return user
