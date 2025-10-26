import aiohttp
import random
import asyncio
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.models import Country
from app.services.image_gen import generate_summary_image
from app.utils.errors import ExternalAPIError, InternalServerError

COUNTRIES_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
RATES_URL = "https://open.er-api.com/v6/latest/USD"
TIMEOUT = 30  

async def fetch_api_data(session: aiohttp.ClientSession, url: str, api_name: str) -> Dict[str, Any]:
    try:
        async with session.get(url, timeout=TIMEOUT) as resp:
            if resp.status != 200:
                raise ExternalAPIError(api_name)
            return await resp.json()
    except asyncio.TimeoutError:
        raise ExternalAPIError(f"{api_name} (timeout)")
    except aiohttp.ClientError as e:
        raise ExternalAPIError(f"{api_name} ({str(e)})")

async def refresh_countries(db: AsyncSession):
    try:
        async with aiohttp.ClientSession() as session:
            try:
                countries_data = await fetch_api_data(session, COUNTRIES_URL, "Countries API")
                rates_data = await fetch_api_data(session, RATES_URL, "Exchange Rates API")
            except Exception as e:
                raise ExternalAPIError(str(e))

        rates = rates_data.get("rates", {})
        if not rates:
            raise ExternalAPIError("Exchange Rates API returned no data")

        await db.execute(delete(Country))
        await db.commit()

        for data in countries_data:
            try:
                name = data["name"]
                pop = data["population"]
                
                if not data.get("currencies"):
                    continue
                    
                currency = data["currencies"][0]["code"]
                rate = rates.get(currency)
                
                if not rate:
                    continue
                
                multiplier = random.randint(1000, 2000)
                gdp = pop * multiplier / rate

                country_obj = Country(
                    name=name,
                    capital=data.get("capital"),
                    region=data.get("region"),
                    population=pop,
                    currency_code=currency,
                    exchange_rate=rate,
                    estimated_gdp=gdp,
                    flag_url=data.get("flag")
                )

                db.add(country_obj)
            except KeyError as e:
                print(f"Error processing country data: {str(e)}")
                continue

        await db.commit()
        await generate_summary_image(db)
    
    except ExternalAPIError as e:
        raise
    except Exception as e:
        raise InternalServerError(str(e))
