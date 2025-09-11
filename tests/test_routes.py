from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_calcul():
    payload = {
        "operande_1": 6,
        "operande_2": 3,
        "operation": "*"
    }

    response = client.post("/calculs/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["operande_1"] == 6
    assert data["operande_2"] == 3
    assert data["operation"] == "*"
    assert data["resultat"] == 18


def test_division_par_zero():
    response = client.post("/calculs/", json={
        "operande_1": 10,
        "operande_2": 0,
        "operation": "/"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Division par zéro"

def test_operation_invalide():
    response = client.post("/calculs/", json={
        "operande_1": 10,
        "operande_2": 5,
        "operation": "%"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Opération invalide"

def test_donnees_manquantes():
    response = client.post("/calculs/", json={
        "operande_1": 10,
        # operande_2 manquant
        "operation": "+"
    })
    assert response.status_code == 422
    assert "operande_2" in response.json()["detail"][0]["loc"]