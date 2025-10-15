from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import get_all_loggers, create_logger, delete_logger  # ✅ импортированы функции
from ..schemas import LoggerCreate, Logger
from ..auth import require_admin

router = APIRouter(prefix="/loggers", tags=["loggers"])

@router.get("/", response_model=list[Logger])
async def read_loggers(db: AsyncSession = Depends(get_db)):
    return await get_all_loggers(db)

@router.post("/", response_model=Logger)
async def create_new_logger(
    logger: LoggerCreate,
    admin = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await create_logger(db, logger)  # ✅ вызываем напрямую, без crud.

@router.delete("/{logger_id}")
async def remove_logger(
    logger_id: int,
    admin = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    deleted = await delete_logger(db, logger_id)  # ✅ вызываем напрямую, без crud.
    if not deleted:
        raise HTTPException(status_code=404, detail="Logger not found")
    return {"detail": "Deleted"}