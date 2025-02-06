# tests/test_api.py

import pytest
import json
from PhobiaApp.scripts.main import app

@pytest.fixture
def client():
    """
    A Pytest fixture that provides a test client for our Flask app.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_phobia_details(client):
    """
    Test the /phobia/<phobia_name> endpoint.
    We assume a known phobia 'Arachnophobia' is in the db for test.
    """
    response = client.get("/phobia/Arachnophobia")
    assert response.status_code == 200 
    assert b"Arachnophobia" in response.data  

def test_get_phobia_symptoms(client):
    response = client.get("/symptoms/Arachnophobia")
    assert response.status_code == 200

    symptoms_list = json.loads(response.data)
    assert isinstance(symptoms_list, list)

    returned_symptoms = set(symptoms_list)

    # Check that each expected symptom is in returned_symptoms
    expected_symptoms = {"panic attack", "chills", "rapid heartbeat", "lightheaded"}
    for symptom in expected_symptoms:
        assert symptom in returned_symptoms, f"Expected symptom '{symptom}' not found."

