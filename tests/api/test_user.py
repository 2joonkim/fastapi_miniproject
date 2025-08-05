def test_get_users(client):
    """사용자 목록 조회 테스트"""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == {"message": "Get all users"}


def test_create_user(client):
    """사용자 생성 테스트"""
    response = client.post("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == {"message": "Create user"}


def test_get_user(client):
    """특정 사용자 조회 테스트"""
    user_id = 1
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Get user {user_id}"}
