.PHONY: test lint format check install dev-up dev-down prod-up prod-down

# 의존성 설치
install:
	uv sync --group dev

# 코드 포맷팅 적용
format:
	uv run black .
	uv run ruff format .

# 린팅 검사
lint:
	uv run ruff check .

# 포맷팅 검사
format-check:
	uv run black --check .
	uv run ruff format --check .

# 테스트 실행
test:
	uv run pytest -v

# 모든 검사 실행 (CI와 동일)
check: lint format-check test
	@echo "All checks passed!"

# 개발용 - 포맷팅 적용 후 검사
dev-check: format check

# Docker 개발환경
dev-up:
	docker-compose -f docker-compose.dev.yml up --build

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Docker 배포환경
prod-up:
	docker-compose up --build -d

prod-down:
	docker-compose down

prod-logs:
	docker-compose logs -f

# 데이터베이스 관련 (Docker 컨테이너 내에서 실행)
db-migrate:
	docker-compose -f docker-compose.dev.yml exec app uv run aerich migrate --name "$(name)"
	
db-upgrade:
	docker-compose -f docker-compose.dev.yml exec app uv run aerich upgrade

db-init:
	docker-compose -f docker-compose.dev.yml exec app uv run aerich init-db

# 로컬에서 실행 (PostgreSQL이 localhost에서 실행될 때)
db-migrate-local:
	uv run aerich migrate --name "$(name)"
	
db-upgrade-local:
	uv run aerich upgrade

# 전체 개발 환경 설정
dev-setup: install dev-up
	@echo "Development environment is ready!"