from fastapi.testclient import TestClient

from python_service_template.main import create_application


def test_health_endpoint():
    app = create_application()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
