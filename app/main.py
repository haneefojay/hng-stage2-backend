from fastapi import FastAPI
from fastapi import FastAPI
from app.routes.countries import router as countries_router
from app.routes.status import router as status_router
from app.routes.image import router as image_router
from app.database import Base, engine

app = FastAPI(title="HNG Stage 2 Backend Task")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(countries_router, prefix="/countries")
app.include_router(status_router)
app.include_router(image_router)
