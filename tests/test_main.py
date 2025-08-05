def test_read_root(client):
    """메인 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI Mini Project!"}


def test_health_check(client):
    """헬스 체크 테스트"""
    response = client.get("/")
    assert response.status_code == 200
