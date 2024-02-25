from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.db import Base 

from .config.db import engine

from .routers import event

app = FastAPI(
    title = "lab3pi",
    docs_url = "/documentation",
    redoc_url = None
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(event.router)