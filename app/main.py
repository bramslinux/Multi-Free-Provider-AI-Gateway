from fastapi import FastAPI
from app.routers.chat import router as chat_router

app = FastAPI(
    title= "Multi-Provider AI Gateway",
    version="1.0"
)

app.include_router(chat_router,prefix="/api")

@app.get("/")
def heath():
    return {"status":"pending"}