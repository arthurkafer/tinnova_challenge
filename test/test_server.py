import json
import pytest
from server import api as app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Vehicles" in response.data or b"vehicle" in response.data

def test_get_all_vehicles(client):
    response = client.get('/veiculos')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_post_new_vehicle(client):
    data = {
        "marca": "Toyota",
        "veiculo": "Corolla",
        "ano": 2020,
        "cor": "prata",
        "vendido": False,
        "descricao": "Sedan confiável"
    }
    response = client.post('/veiculos', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["marca"] == "Toyota"

def test_chart_data_endpoint(client):
    response = client.get('/api/chart_data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "decades" in json_data
    assert "brands" in json_data