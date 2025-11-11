from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    tg_id = Column(Integer, nullable=True)
    role = Column(Enum("admin", "user", name="user_role"), default="user")

class Logger(Base):
    __tablename__ = "loggers"
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(100), unique=True, index=True)
    description = Column(String(255), nullable=True)

class LoggerData(Base):
    __tablename__ = "logger_data"
    id = Column(Integer, primary_key=True, index=True)
    logger_id = Column(Integer, ForeignKey("loggers.id"))
    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    power = Column(Float, nullable=False)
    illuminance = Column(Float, nullable=False)
    isMaxPoint = Column(Boolean, default=False)
    chunkName = Column(String(255), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())