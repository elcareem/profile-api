from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from .models.base import Base
from .routes.user import router as user_router
from .routes.auth import router as auth_router

app = FastAPI() 
 
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)


app.mount("/static", StaticFiles(directory="static"), name="static")
