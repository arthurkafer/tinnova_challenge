import pytest
from cars_app import CarsApp, InvalidUsage

@pytest.fixture
def app():
    return CarsApp()

def test_get_all_vehicles(app):
    vehicles = app.get_all_vehicles()
    assert isinstance(vehicles, list)
    assert len(vehicles) >= 1

def test_add_vehicle_success(app):
    vehicle = {
        "marca": "Fiat",
        "veiculo": "Uno",
        "ano": 2005,
        "cor": "azul",
        "vendido": False,
        "descricao": "Econômico"
    }
    result = app.add_vehicle(vehicle)
    assert result["marca"] == "Fiat"
    assert "id" in result

def test_add_vehicle_missing_field(app):
    with pytest.raises(InvalidUsage) as exc:
        app.add_vehicle({
            "marca": "Fiat",
            "veiculo": "Uno",
            "ano": 2005,
            "cor": "azul",
            # Missing 'vendido' and 'descricao'
        })
    assert exc.value.status_code == 422

def test_update_nonexistent_vehicle(app):
    with pytest.raises(InvalidUsage) as exc:
        app.update_vehicle({"cor": "verde"}, "nonexistent-id")
    assert exc.value.status_code == 404

def test_delete_vehicle_success(app):
    vehicle = app.add_vehicle({
        "marca": "Ford",
        "veiculo": "Ka",
        "ano": 2010,
        "cor": "branco",
        "vendido": False,
        "descricao": "Carro pequeno"
    })
    deleted = app.delete_vehicle(vehicle["id"])
    assert deleted["id"] == vehicle["id"]