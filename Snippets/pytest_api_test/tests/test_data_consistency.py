import requests

def test_update_post(base_url):
    post_id = 1
    payload = {"title": "Updated Title"}
    response = requests.patch(f"{base_url}/posts/{post_id}", json=payload)
    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["title"] == "Updated Title"
