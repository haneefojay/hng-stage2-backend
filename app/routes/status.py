from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.database import get_db
from app.models import Country

router = APIRouter()

@router.get("/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count()).select_from(Country))

    result = await db.execute(
        select(func.max(Country.last_refreshed_at))
    )
    refreshed_at = result.scalar()

    return {
        "total_countries": total,
        "last_refreshed_at": refreshed_at
    }
