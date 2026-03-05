from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

from routers import auth, users, posts, comments, interactions, media

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DTU Confession API", version="1.0.0")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"[FASTAPI VALIDATION ERROR] {exc.errors()}")
    print(f"[FASTAPI VALIDATION BODY] {exc.body}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": str(exc.body)},
    )


# CORS — cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(interactions.router)
app.include_router(media.router)


@app.get("/")
def read_root():
    return {"status": "success", "message": "DTU Confession API is running!"}