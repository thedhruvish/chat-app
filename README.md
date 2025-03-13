# 📱 FastChat - A WhatsApp-like Messaging App (Python + FastAPI)

FastChat is a real-time messaging web app inspired by WhatsApp. It leverages modern Python web technologies including **FastAPI**, **Starlette**, **Google OAuth2**, **SQLite3**, and **Uvicorn** for fast and scalable performance.

---

## 🚀 Features

- ✅ Google OAuth2 login
- 💬 Real-time chat features
- 🗃️ SQLite3-based local database
- 🧠 Modular architecture with routers and utils
- 🔐 Custom middleware for logging and auth
- ⚡ FastAPI + Uvicorn (via `uv`) backend
- 🖥️ Jinja2 templating for UI

---

## 🧰 Tech Stack

| Tech             | Use Case                     |
|------------------|------------------------------|
| FastAPI          | Web framework (REST APIs)    |
| Starlette        | Middleware & ASGI support    |
| SQLite3          | Lightweight database         |
| Google OAuth2    | User authentication          |
| Jinja2           | HTML templating              |
| uv + uvicorn     | Package manager & ASGI server|

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/thedhruvish/chat-app.git
cd chat-app

# Install dependencies with uv
uv venv
source venv/bin/activate # active the virtual environment
uv install

# Run the app
fastapi run app/app.py
```

---

## 📂 Project Structure

```
chat-app/
│
├── app/
│   ├── db/
│   │   └── sqllit_db.py          # SQLite3 DB connection
│   ├── router/
│   │   ├── auth.py               # Google OAuth2 auth routes
│   │   └── chat.py               # Chat-related endpoints
│   ├── schemas/
│   │   └── user.py               # User models (Pydantic)
│   ├── templates/                # HTML templates
│   └── utile/
│       └── chat_manage.py        # Chat management logic
│
├── .env                          # Environment variables
├── .gitignore
├── .python-version
├── chat.db                       # SQLite3 database
├── LICENSE
├── pyproject.toml                # Project dependencies
├── uv.lock                       # Locked dependencies
└── README.md                     # Project documentation

```

---

## 🧪 Usage

- Visit `http://localhost:8000`
- Click "Login with Google"
- Start chatting!

---

## 📃 License

MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Contributing

Contributions are welcome! Please fork the repo and submit a pull request.

---

## 📬 Contact

Created by [@thedhruvish](https://github.com/thedhruvish) – feel free to reach out!
email - [thedhruvish@gmail.com](mailto:thedhruvish@gmail.com)



