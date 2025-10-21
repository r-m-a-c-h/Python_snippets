import requests

def test_response_time(base_url):
    response = requests.get(f"{base_url}/posts")
    assert response.elapsed.total_seconds() < 0.5  # less than 500ms response time
