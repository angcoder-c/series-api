from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth_router import router as auth_router
from src.api.rating_router import router as rating_router
from src.api.series_router import router as series_router
from src.api.genre_router import router as genre_router

app = FastAPI(title="Series API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(series_router)
app.include_router(genre_router)
app.include_router(rating_router)


@app.get("/")
async def root():
    return {"msg": "Series API running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
