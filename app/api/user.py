from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.repositories.user_repository import UserRepository
from app.models import User

router = APIRouter()

def get_user_repository() -> UserRepository:
    return UserRepository()

@router.get("/users/")
async def get_users(
    optimized: bool = Query(False, description="N+1 문제 해결 여부"),
    repo: UserRepository = Depends(get_user_repository)
):
    """사용자 목록 조회 (N+1 문제 해결 옵션)"""
    if optimized:
        users = await repo.get_all_users_optimized()
        return {
            "message": "Users fetched with optimization (prefetch_related)",
            "users": [{"id": u.id, "name": u.name, "email": u.email} for u in users]
        }
    else:
        users = await repo.get_all_users()
        return {
            "message": "Users fetched without optimization (N+1 problem)",
            "users": [{"id": u.id, "name": u.name, "email": u.email} for u in users]
        }

@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    with_posts: bool = Query(False, description="게시글 포함 여부"),
    repo: UserRepository = Depends(get_user_repository)
):
    """사용자 상세 조회"""
    if with_posts:
        user = await repo.get_user_with_posts(user_id)
    else:
        user = await repo.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = {"id": user.id, "name": user.name, "email": user.email}
    
    if with_posts:
        await user.fetch_related("posts")
        result["posts"] = [
            {"id": p.id, "title": p.title} 
            for p in user.posts
        ]
    
    return result

@router.post("/users/")
async def create_user(
    name: str,
    email: str,
    repo: UserRepository = Depends(get_user_repository)
):
    """사용자 생성"""
    user = await repo.create_user(name=name, email=email)
    return {"id": user.id, "name": user.name, "email": user.email}

@router.post("/users/bulk")
async def bulk_create_users(
    users_data: List[dict],
    repo: UserRepository = Depends(get_user_repository)
):
    """대량 사용자 생성 (bulk_create 최적화)"""
    users = await repo.bulk_create_users(users_data)
    return {
        "message": f"Created {len(users)} users using bulk_create",
        "users": [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    }

@router.get("/users/stats/post-count")
async def get_users_with_post_count(
    repo: UserRepository = Depends(get_user_repository)
):
    """사용자별 게시글 수 집계 (annotate 사용)"""
    stats = await repo.get_users_with_post_count()
    return {
        "message": "User post count statistics using annotate",
        "stats": stats
    }

@router.get("/users/names-only")
async def get_user_names_only(
    repo: UserRepository = Depends(get_user_repository)
):
    """사용자 이름만 조회 (values 최적화)"""
    names = await repo.get_user_names_only()
    return {
        "message": "User names only using values optimization",
        "names": names
    }