import requests

def test_get_posts(base_url):
    response = requests.get(f"{base_url}/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "userId" in data[0]

def test_create_post(base_url):
    payload = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(f"{base_url}/posts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "foo"
