import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class QueryMonitorMiddleware(BaseHTTPMiddleware):
    """쿼리 성능 모니터링 미들웨어"""

    def __init__(self, app):
        super().__init__(app)
        self.query_stats: list[dict] = []

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # 쿼리 카운터 초기화
        query_count_before = self._get_query_count()

        response = await call_next(request)

        # 실행 시간 계산
        process_time = time.time() - start_time
        query_count_after = self._get_query_count()
        query_count = query_count_after - query_count_before

        # 통계 저장
        stats = {
            "path": request.url.path,
            "method": request.method,
            "process_time": round(process_time, 4),
            "query_count": query_count,
            "timestamp": time.time(),
        }

        self.query_stats.append(stats)

        # 로그 출력
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Time: {process_time:.4f}s, Queries: {query_count}"
        )

        # 응답 헤더에 성능 정보 추가
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Query-Count"] = str(query_count)

        return response

    def _get_query_count(self) -> int:
        """현재 쿼리 수 반환 (실제 구현 필요)"""
        # Tortoise ORM의 쿼리 카운터 구현
        return 0

    def get_stats(self) -> list[dict]:
        """성능 통계 반환"""
        return self.query_stats

    def clear_stats(self):
        """통계 초기화"""
        self.query_stats.clear()
