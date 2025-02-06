import requests
import pytest

@pytest.mark.integration
def test_live_treatment_endpoint():
    url = "http://alexocegueda.pythonanywhere.com/treatments/Arachnophobia"
    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()  
    assert isinstance(data, list), "Expected a JSON list from /treatments/<phobia_name>"

    assert "psychotherapy" in data, "Expected 'psychotherapy' in returned treatments"
    assert "exposure therapy" in data, "Expected 'exposure therapy' in returned treatments"

@pytest.mark.integration
def test_live_symptom_endpoint():
    """
    This test calls the live /symptoms/<phobia_name> endpoint hosted on PythonAnywhere.

    It verifies:
      - HTTP 200 status
      - The response is valid JSON (list)
      - The returned symptoms match our expectations for 'Arachnophobia'
    """
    url = "http://alexocegueda.pythonanywhere.com/symptoms/Arachnophobia"
    response = requests.get(url)
    assert response.status_code == 200, "Expected a 200 response from the live endpoint."

    symptoms_data = response.json()  
    assert isinstance(symptoms_data, list), "Expected a JSON list from /symptoms/<phobia_name>."

    expected_symptoms = {"panic attack", "chills", "rapid heartbeat", "lightheaded"}
    returned_symptoms = set(symptoms_data)
    for symptom in expected_symptoms:
        assert symptom in returned_symptoms, f"Expected '{symptom}' in the live endpoint response."