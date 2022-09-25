from fastapi import FastAPI

from database import Base, engine
from routers import job_posts, user

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def root():
    return "Hello Nuwe!"


app.include_router(job_posts.router, tags=["API"], prefix="/API/v1/jobposts")
app.include_router(user.router, tags=["users"], prefix="/API/v1/users")
