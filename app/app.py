from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth, chat
from app.db.sqllit_db import Connection


@asynccontextmanager
async def lifespan(app: FastAPI):
	app.state.db = Connection()
	print("📦 Database initialized.")
	yield
	app.state.db.close()
	print("❌ Database connection closed.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="!secret")


@app.get("/", response_class=RedirectResponse)
def home():
	return RedirectResponse("/auth")


app.include_router(auth.route, prefix="/auth")

app.include_router(chat.route, prefix="/chat")
