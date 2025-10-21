import requests

def test_create_user_missing_fields(base_url):
    payload = {"username": "test_user"}  # missing required fields
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 400
    error = response.json()
    assert "error" in error