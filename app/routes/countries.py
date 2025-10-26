from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Country
from sqlalchemy import select, desc, func, asc
from app.services.refresh import refresh_countries
from app.utils.errors import NotFoundError, InternalServerError
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
        stmt = stmt.where(func.lower(Country.region) == region.lower())

    if currency:
        stmt = stmt.where(func.lower(Country.currency_code) == currency.lower())

    if sort == "gdp_desc":
        stmt = stmt.order_by(desc(Country.estimated_gdp).nulls_last())
    elif sort == "gdp_asc":
        stmt = stmt.order_by(asc(Country.estimated_gdp).nulls_last())

    result = await db.execute(stmt)
    countries = result.scalars().all()
    
    if not countries:
        raise NotFoundError()
        
    return countries


@router.get("/countries/{name}")
async def get_country(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Country).filter(Country.name.ilike(name))
    )
    country = result.scalar_one_or_none()

    if not country:
        raise NotFoundError()

    return country


@router.delete("/countries/{name}", status_code=204)
async def delete_country(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Country).filter(Country.name.ilike(name))
    )
    country = result.scalar_one_or_none()

    if not country:
        raise NotFoundError()

    try:
        await db.delete(country)
        await db.commit()
        return {"message": f"{name} deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise InternalServerError(f"Failed to delete country: {str(e)}")
