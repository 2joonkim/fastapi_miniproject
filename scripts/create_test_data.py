"""테스트 데이터 생성 스크립트"""

import asyncio

from tortoise import Tortoise

from app.database import TORTOISE_ORM
from app.models import Comment, Post, Profile, User


async def create_test_data():
    """N+1 문제 테스트를 위한 데이터 생성"""
    await Tortoise.init(config=TORTOISE_ORM)

    print("Creating test data...")

    # 사용자 10명 생성
    users = []
    for i in range(1, 11):
        user = await User.create(name=f"User {i}", email=f"user{i}@example.com")
        users.append(user)

        # 각 사용자마다 프로필 생성
        await Profile.create(
            user=user,
            bio=f"Bio for user {i}",
            avatar_url=f"https://example.com/avatar{i}.jpg",
        )

        # 각 사용자마다 게시글 3-5개 생성
        for j in range(1, 4):
            post = await Post.create(
                title=f"Post {j} by User {i}",
                content=f"Content of post {j} by user {i}",
                user=user,
            )

            # 각 게시글마다 댓글 2-3개 생성
            for k in range(1, 3):
                await Comment.create(
                    content=f"Comment {k} on post {j}",
                    post=post,
                    user=users[k % len(users)],  # 다른 사용자가 댓글 작성
                )

    print("Test data created successfully!")
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(create_test_data())
