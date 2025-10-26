from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from app.models import Country
import os
from datetime import datetime

CACHE_PATH = "cache"
IMAGE_PATH = f"{CACHE_PATH}/summary.png"

async def generate_summary_image(db: AsyncSession):
    os.makedirs(CACHE_PATH, exist_ok=True)
    
    total = await db.scalar(select(func.count()).select_from(Country))

    result = await db.execute(
        select(Country).where(Country.estimated_gdp != None).order_by(desc(Country.estimated_gdp)).limit(5)
    )
    top_countries = result.scalars().all()

    img = Image.new("RGB", (900, 500), color=(20, 20, 25))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_text = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    draw.text((20, 20), "HNG Stage 2 - Country Summary", font=font_title, fill=(255, 255, 255))
    draw.text((20, 80), f"Total Countries: {total}", font=font_text, fill=(200, 255, 200))

    y = 140
    draw.text((20, y), "Top 5 by Estimated GDP:", font=font_text, fill=(255, 255, 0))
    y += 40

    for c in top_countries:
        draw.text((20, y), f"{c.name} — {round(c.estimated_gdp, 2)}", font=font_text, fill=(255, 255, 255))
        y += 30

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    draw.text((20, 440), f"Last Refreshed: {timestamp}", font=font_text, fill=(150, 150, 150))

    img.save(IMAGE_PATH)
    return IMAGE_PATH
