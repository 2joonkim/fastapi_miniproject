"""N+1 문제 테스트 스크립트"""
import asyncio
import time
from tortoise import Tortoise
from app.database import TORTOISE_ORM
from app.models import User

# 쿼리 로깅 설정
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("tortoise.db_client")

async def test_n_plus_1_problem():
    """N+1 문제 발생 테스트"""
    await Tortoise.init(config=TORTOISE_ORM)
    
    print("=" * 50)
    print("N+1 문제 발생 테스트")
    print("=" * 50)
    
    start_time = time.time()
    
    # N+1 문제 발생: 사용자 조회 후 각각의 게시글을 개별 쿼리로 조회
    users = await User.all()  # 1번 쿼리
    
    for user in users:  # N번 쿼리 (사용자 수만큼)
        posts = await user.posts.all()
        print(f"User: {user.name}, Posts: {len(posts)}")
    
    end_time = time.time()
    print(f"실행 시간: {end_time - start_time:.4f}초")
    print(f"예상 쿼리 수: 1 + {len(users)} = {1 + len(users)}개")
    
    await Tortoise.close_connections()

async def test_optimized_query():
    """최적화된 쿼리 테스트"""
    await Tortoise.init(config=TORTOISE_ORM)
    
    print("\n" + "=" * 50)
    print("최적화된 쿼리 테스트 (prefetch_related)")
    print("=" * 50)
    
    start_time = time.time()
    
    # 최적화: prefetch_related로 한 번에 조회
    users = await User.all().prefetch_related("posts")  # 2번 쿼리만 실행
    
    for user in users:
        posts = user.posts  # 추가 쿼리 없음
        print(f"User: {user.name}, Posts: {len(posts)}")
    
    end_time = time.time()
    print(f"실행 시간: {end_time - start_time:.4f}초")
    print("예상 쿼리 수: 2개 (users + posts)")
    
    await Tortoise.close_connections()

async def main():
    """메인 테스트 함수"""
    await test_n_plus_1_problem()
    await test_optimized_query()

if __name__ == "__main__":
    asyncio.run(main())