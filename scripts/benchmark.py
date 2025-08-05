#!/usr/bin/env python3
"""API 성능 벤치마크 스크립트"""

import asyncio
import time
from statistics import mean, median

import aiohttp


async def measure_response_time(session, url, iterations=10):
    """API 응답시간 측정"""
    times = []

    for _ in range(iterations):
        start_time = time.time()
        async with session.get(url) as response:
            await response.text()
            end_time = time.time()
            times.append(end_time - start_time)

        # 요청 간 간격
        await asyncio.sleep(0.1)

    return {
        "url": url,
        "iterations": iterations,
        "times": times,
        "avg": mean(times),
        "median": median(times),
        "min": min(times),
        "max": max(times),
    }


async def benchmark_apis():
    """N+1 문제 전후 성능 비교"""
    base_url = "http://localhost:8000/api/v1/users/"

    urls = {
        "N+1 문제 (최적화 없음)": f"{base_url}?optimized=false",
        "최적화됨 (prefetch_related)": f"{base_url}?optimized=true",
        "사용자별 게시글 수": "http://localhost:8000/api/v1/users/stats/post-count",
        "이름만 조회": "http://localhost:8000/api/v1/users/names-only",
    }

    async with aiohttp.ClientSession() as session:
        print("🚀 API 성능 벤치마크 시작...")
        print("=" * 60)

        results = {}
        for name, url in urls.items():
            try:
                print(f"📊 {name} 측정 중...")
                result = await measure_response_time(session, url, iterations=5)
                results[name] = result

                print(f"   평균: {result['avg']:.4f}초")
                print(f"   최소: {result['min']:.4f}초")
                print(f"   최대: {result['max']:.4f}초")
                print()

            except Exception as e:
                print(f"❌ {name} 측정 실패: {e}")
                print()

        # 비교 결과 출력
        if (
            "N+1 문제 (최적화 없음)" in results
            and "최적화됨 (prefetch_related)" in results
        ):
            n_plus_1_time = results["N+1 문제 (최적화 없음)"]["avg"]
            optimized_time = results["최적화됨 (prefetch_related)"]["avg"]
            improvement = ((n_plus_1_time - optimized_time) / n_plus_1_time) * 100

            print("📈 성능 개선 결과:")
            print(f"   N+1 문제: {n_plus_1_time:.4f}초")
            print(f"   최적화됨: {optimized_time:.4f}초")
            print(f"   개선율: {improvement:.1f}% 향상")


if __name__ == "__main__":
    asyncio.run(benchmark_apis())
