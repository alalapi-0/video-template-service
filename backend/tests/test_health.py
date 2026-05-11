"""
最小测试：确认 /health 可访问（需在 backend 目录下安装依赖后运行 pytest）。
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["service"] == "video-template-service"
