import json
import app
 
def test_get_users(monkeypatch):
    # Mock DB call
    def fake_get_users():
        return ["Manish", "SkillShikshya"]
    monkeypatch.setattr(app, "get_users", fake_get_users)
 
    client = app.app.test_client()
    response = client.get("/api/users")
    data = json.loads(response.data)
    assert "Manish" in data
    assert "SkillShikshya" in data
 
def test_add_user(monkeypatch):
    # Mock DB insert
    def fake_get_connection():
        class FakeConn:
            def cursor(self): return self
            def execute(self, q, args=None): pass
            def commit(self): pass
            def close(self): pass
        return FakeConn()
    monkeypatch.setattr(app, "get_connection", fake_get_connection)
 
    client = app.app.test_client()
    response = client.post("/api/users", json={"name": "NewStudent"})
    data = json.loads(response.data)
    assert response.status_code == 201
    assert "NewStudent" in data["message"]