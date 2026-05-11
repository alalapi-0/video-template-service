"""Round 1：任务接口的校验逻辑回归测试（上传、模板 ID）。"""

from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from app.core import config


@pytest.fixture
def client(monkeypatch, tmp_path):
    """减小上传限额，便于在测试中构造「超限」样本，并把文件写到临时路径。"""
    uploads = tmp_path / "uploads"
    outputs = tmp_path / "outputs"
    uploads.mkdir()
    outputs.mkdir()

    monkeypatch.setattr(config, "STORAGE_UPLOADS", uploads)
    monkeypatch.setattr(config, "STORAGE_OUTPUTS", outputs)

    monkeypatch.setattr(config, "MAX_UPLOAD_BYTES", 4096)

    # 延迟导入以便前面的 monkeypatch 生效
    from app.main import app

    return TestClient(app)


def test_create_job_happy_path(client: TestClient):
    payload = {
        "user_text": "演示文案",
        "template_id": "vertical_short_video_v1",
    }
    files = {
        "main_video": ("demo.mp4", BytesIO(b"fake-mp4-body"), "video/mp4"),
    }

    response = client.post("/jobs", data=payload, files=files)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "queued"
    assert body["job_id"]

    detail = client.get(f"/jobs/{body['job_id']}").json()
    assert detail["status"] == "completed"
    assert detail["output_url"].startswith("http://testserver/outputs/mock-result.mp4")


def test_create_job_bad_template(client: TestClient):
    payload = {
        "user_text": "演示文案",
        "template_id": "not-exist",
    }
    files = {
        "main_video": ("demo.mp4", BytesIO(b"x"), "video/mp4"),
    }
    response = client.post("/jobs", data=payload, files=files)
    assert response.status_code == 400
    assert response.json()["detail"]


def test_create_job_bad_suffix(client: TestClient):
    payload = {
        "user_text": "演示文案",
        "template_id": "vertical_short_video_v1",
    }
    files = {
        "main_video": ("note.txt", BytesIO(b"hello"), "text/plain"),
    }
    response = client.post("/jobs", data=payload, files=files)
    assert response.status_code == 400


def test_create_job_too_large(client: TestClient, monkeypatch):
    monkeypatch.setattr("app.services.video_service.MAX_UPLOAD_BYTES", 16)
    payload = {"user_text": "x", "template_id": "vertical_short_video_v1"}
    body = b"0" * 64
    files = {"main_video": ("demo.mp4", BytesIO(body), "video/mp4")}
    response = client.post("/jobs", data=payload, files=files)
    assert response.status_code == 413
