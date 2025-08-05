from fastapi import APIRouter

router = APIRouter()


@router.get("/users/")
async def get_users():
    return {"message": "Simple users endpoint working"}


@router.get("/users/test")
async def test_endpoint():
    return {"status": "API is working", "database": "not connected yet"}
