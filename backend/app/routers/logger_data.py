from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..crud import create_logger_data, get_logger_data_by_logger_id, get_logger_by_identifier
from ..schemas import LoggerDataBatch, LoggerDataOut
from ..auth import get_current_user
from ..models import Logger
from datetime import datetime
import pandas as pd
from io import StringIO

router = APIRouter(prefix="/data", tags=["data"])

@router.post("/")
async def ingest_data(batch: LoggerDataBatch, db: AsyncSession = Depends(get_db)):
    for item in batch.data:
        await create_logger_data(db, item)
    return {"status": "success", "count": len(batch.data)}

@router.get("/csv")
async def download_csv(
    logger_ids: str = Query(...),
    start: str = None,
    end: str = None,
    db: AsyncSession = Depends(get_db)
):
    ids = [int(x) for x in logger_ids.split(",")]
    all_data = []

    for lid in ids:
        # Получаем identifier логгера
        logger_result = await db.execute(select(Logger).where(Logger.id == lid))
        logger = logger_result.scalars().first()
        if not logger:
            raise HTTPException(status_code=404, detail=f"Logger {lid} not found")

        start_dt = datetime.fromisoformat(start) if start else None
        end_dt = datetime.fromisoformat(end) if end else None
        data = await get_logger_data_by_logger_id(db, lid, start_dt, end_dt)

        for d in data:
            all_data.append({
                "logger_id": lid,
                "logger_identifier": logger.identifier,  # ← добавляем identifier
                "voltage": d.voltage,
                "current": d.current,
                "power": d.power,
                "illuminance": d.illuminance,
                "timestamp": d.timestamp.isoformat()
            })

    df = pd.DataFrame(all_data)

    # Генерируем имя файла: {identifier}_{timestamp}.csv
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{logger.identifier}_{timestamp}.csv"

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/graph/{logger_id}", response_model=list[LoggerDataOut])
async def get_graph_data(
    logger_id: int,
    start: str = None,
    end: str = None,
    db: AsyncSession = Depends(get_db)
):
    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None
    data = await get_logger_data_by_logger_id(db, logger_id, start_dt, end_dt)
    return data