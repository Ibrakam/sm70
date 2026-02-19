from fastapi import FastAPI
from api.photo_api.main import photo_router
from database import Base, engine


app = FastAPI(docs_url="/")
app.include_router(photo_router)

Base.metadata.create_all(engine)