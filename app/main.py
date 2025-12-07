from fastapi import FastAPI
from app.routes import router
from app.config import PORT

app = FastAPI()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Payment API running"}
