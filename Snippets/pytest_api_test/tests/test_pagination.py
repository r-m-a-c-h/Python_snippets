import requests

def test_pagination(base_url):
    params = {"page": 1, "limit": 10}
    response = requests.get(f"{base_url}/items", params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 10
