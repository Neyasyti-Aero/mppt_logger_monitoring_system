import asyncio
from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import logger_data, loggers, users, auth
from .database import engine, async_session
from .models import Base
from .crud import create_user_safe, get_user_by_username, create_user
from .schemas import UserCreate
from .auth import get_password_hash

app = FastAPI(
    title="MPPT Loggers API",
    root_path="/mppt_loggers/api"  # ← ключевая строка
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logger_data.router)
app.include_router(loggers.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.on_event("startup")
async def startup():
    # Ждём готовности БД (опционально)
    for _ in range(30):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            break
        except Exception as e:
            print("⏳ Waiting for DB...", e)
            await asyncio.sleep(2)
    else:
        raise Exception("❌ Database not available")

    # Создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаём админа ТОЛЬКО если его нет
    async with async_session() as db:
        admin_user = UserCreate(
            username="admin",
            password="admin",  # ← keep it short!
            role="admin"
        )
        admin = await create_user_safe(db, admin_user)
        if admin.username == "admin":
            print("✅ Админ создан или уже существует")