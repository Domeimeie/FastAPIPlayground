def test_authenticate(client):
    client.post("/users", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    response = client.post("/auth/login", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    assert response.status_code == 200
    assert response.json() == {"ok": True}
