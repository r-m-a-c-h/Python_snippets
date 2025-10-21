import requests

def test_invalid_endpoint(base_url):
    response = requests.get(f"{base_url}/invalid-endpoint")
    assert response.status_code == 404

def test_wrong_http_method(base_url):
    response = requests.put(f"{base_url}/posts/1")  # assuming PUT not supported
    assert response.status_code in (400, 405)
