from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Country
from sqlalchemy import select, desc
from app.services.refresh import refresh_countries
from typing import Optional

router = APIRouter()

@router.get("/")
async def get_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    return result.scalars().all()


@router.post("/refresh")
async def refresh(db: AsyncSession = Depends(get_db)):
    await refresh_countries(db)
    return {"message": "Countries refreshed successfully"}


@router.get("/countries")
async def get_countries(
    region: Optional[str] = None,
    currency: Optional[str] = None,
    sort: Optional[str] = Query(None, description="gdp_desc or gdp_asc"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Country)

    if region:
        stmt = stmt.where(Country.region.ilike(region))

    if currency:
        stmt = stmt.where(Country.currency_code.ilike(currency))

    if sort == "gdp_desc":
        stmt = stmt.order_by(desc(Country.estimated_gdp))
    elif sort == "gdp_asc":
        stmt = stmt.order_by(Country.estimated_gdp)

    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/countries/{name}")
async def get_country(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Country).where(Country.name.ilike(name))
    )
    country = result.scalar_one_or_none()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    return country


@router.delete("/countries/{name}")
async def delete_country(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Country).where(Country.name.ilike(name))
    )
    country = result.scalar_one_or_none()

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    await db.delete(country)
    await db.commit()

    return {"message": f"{name} deleted successfully"}
