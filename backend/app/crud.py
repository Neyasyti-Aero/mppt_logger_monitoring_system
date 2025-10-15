from sqlalchemy.future import select
from sqlalchemy import and_
from datetime import datetime, timedelta
from .models import User, Logger, LoggerData
from .schemas import UserCreate, LoggerCreate, LoggerDataCreate
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_password_hash
from sqlalchemy.exc import IntegrityError

async def create_user_safe(db: AsyncSession, user: UserCreate):
    """Create user only if not exists — safe for concurrent calls."""
    db_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        tg_id=user.tg_id,
        role=user.role
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        # User already exists — return existing one
        return await get_user_by_username(db, user.username)

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        username=user.username,
        tg_id=user.tg_id,
        role=user.role,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def delete_user(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user

# Loggers
async def get_logger_by_identifier(db: AsyncSession, identifier: str):
    result = await db.execute(select(Logger).where(Logger.identifier == identifier))
    return result.scalars().first()

async def create_logger(db: AsyncSession, logger: LoggerCreate):
    db_logger = Logger(**logger.dict())
    db.add(db_logger)
    await db.commit()
    await db.refresh(db_logger)
    return db_logger

async def get_all_loggers(db: AsyncSession):
    result = await db.execute(select(Logger))
    return result.scalars().all()

async def delete_logger(db: AsyncSession, logger_id: int):
    logger = await db.get(Logger, logger_id)
    if logger:
        await db.delete(logger)
        await db.commit()
    return logger

# Logger Data
async def create_logger_data(db: AsyncSession, data: LoggerDataCreate):
    logger = await get_logger_by_identifier(db, data.identifier)
    if not logger:
        logger = Logger(identifier=data.identifier)
        db.add(logger)
        await db.commit()
        await db.refresh(logger)
    db_data = LoggerData(
        logger_id=logger.id,
        voltage=data.voltage,
        current=data.current,
        power=data.power,
        illuminance=data.illuminance
    )
    db.add(db_data)
    await db.commit()
    await db.refresh(db_data)
    return db_data

async def get_logger_data_by_logger_id(db: AsyncSession, logger_id: int, start: datetime = None, end: datetime = None):
    query = select(LoggerData).where(LoggerData.logger_id == logger_id)
    if start:
        query = query.where(LoggerData.timestamp >= start)
    if end:
        query = query.where(LoggerData.timestamp <= end)
    query = query.order_by(LoggerData.timestamp)
    result = await db.execute(query)
    return result.scalars().all()