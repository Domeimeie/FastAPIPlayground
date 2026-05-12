import jwt

def test_authenticate(client):
    client.post("/users", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    response = client.post("/auth/login", json={"email": "dodododododod@dododod.local", "password":"gagagagaga"})
    assert response.status_code == 200
    token=response.json()
    payload=jwt.decode(token, "secret", algorithms=["HS256"])
    assert payload["user.id"] == 1
