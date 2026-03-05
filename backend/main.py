from fastapi import FastAPI
from database import engine
import models

from routers import auth, users, posts, comments, interactions

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DTU Confession API", version="1.0.0")

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(interactions.router)


@app.get("/")
def read_root():
    return {"status": "success", "message": "DTU Confession API is running!"}