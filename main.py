"""Aplicación FastAPI."""
from fastapi import FastAPI
from src.api.auth_router import router as auth_router
from src.api.series_router import router as series_router

app = FastAPI(title="Series API")

app.include_router(auth_router)
app.include_router(series_router)


@app.get("/")
async def root():
    return {"msg": "Series API running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
