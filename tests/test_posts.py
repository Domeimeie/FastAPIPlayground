def test_get_post_detail(client, first_post_by_homer):
    response = client.get(f"/posts/{first_post_by_homer.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == first_post_by_homer.id
    assert data["title"] == first_post_by_homer.title

def test_post_not_found(client):
    response = client.get("/posts/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Post not found"