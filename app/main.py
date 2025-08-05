from fastapi import FastAPI

from app.api import user

# from app.database import init_db

app = FastAPI(title="FastAPI Mini Project", version="1.0.0")

# 라우터 등록
app.include_router(user.router, prefix="/api/v1", tags=["users"])

# @app.on_event("startup")
# async def startup_event():
#     await init_db()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Mini Project!"}
