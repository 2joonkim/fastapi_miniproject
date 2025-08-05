from typing import List, Optional
from tortoise.queryset import QuerySet
from tortoise.functions import Count
from app.models import User, Post

class UserRepository:
    """사용자 데이터 접근 계층"""
    
    async def get_all_users(self) -> List[User]:
        """모든 사용자 조회 (N+1 문제 발생)"""
        return await User.all()
    
    async def get_all_users_optimized(self) -> List[User]:
        """모든 사용자 조회 (N+1 문제 해결)"""
        return await User.all().prefetch_related("posts", "profile")
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """사용자 ID로 조회"""
        return await User.filter(id=user_id).first()
    
    async def get_user_with_posts(self, user_id: int) -> Optional[User]:
        """사용자와 게시글 함께 조회 (N+1 문제 해결)"""
        return await User.filter(id=user_id).prefetch_related("posts").first()
    
    async def create_user(self, name: str, email: str) -> User:
        """사용자 생성"""
        return await User.create(name=name, email=email)
    
    async def bulk_create_users(self, users_data: List[dict]) -> List[User]:
        """대량 사용자 생성 (bulk_create 최적화)"""
        users = [User(**data) for data in users_data]
        return await User.bulk_create(users)
    
    async def get_users_with_post_count(self) -> QuerySet:
        """사용자별 게시글 수 집계 (annotate 사용)"""
        return await User.all().annotate(
            post_count=Count("posts")
        ).values("id", "name", "email", "post_count")
    
    async def get_user_names_only(self) -> List[dict]:
        """사용자 이름만 조회 (values 최적화)"""
        return await User.all().values("id", "name")
