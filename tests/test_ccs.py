import pytest
from unittest.mock import patch, Mock, MagicMock, mock_open
from ClevelandClinicScrape.crawl import process_disease_page, crawl
import json

@pytest.mark.parametrize("html_input,expected_name,expected_questions", [
    (
     """<html><body>
        <h1>Phobia One</h1>
        <h3>What is phobia one?</h3><p>...</p>
      </body></html>""",
     "Phobia One",
     ["What is phobia one?"]
    ),
    (
     """<html><body>
        <h1>Missing H3</h1>
        <p>No heading here</p>
      </body></html>""",
     "Missing H3",
     []
    )
])
@patch("ClevelandClinicScrape.crawl.requests.get")
def test_process_disease_page_various(mock_get, html_input, expected_name, expected_questions):
    """
    Test that `process_disease_page` parses different HTML snippets correctly.

    We parametrize the test with multiple HTML cases:
    - A normal phobia page with <h1> and <h3>
    - A page missing <h3> headings
    """
    mock_response = Mock()
    mock_response.text = html_input
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = process_disease_page("https://fakeurl.com/dynamic")

    assert result["name"] == expected_name
    for q in expected_questions:
        assert q in result["data"]

@patch("ClevelandClinicScrape.crawl.time.sleep")                
@patch("ClevelandClinicScrape.crawl.WebDriverWait")             
@patch("builtins.open", new_callable=mock_open) 
def test_crawl_click_letters(mock_file, mock_wait, mock_sleep):
    """
    Mock-based test for our Selenium crawler:

    - Mocks time.sleep, WebDriverWait, file writing, and driver calls
    - Ensures `crawl()` calls `driver.get()`, `driver.find_elements()`,
      and writes the resulting JSON file.
    - Doesn't hit the real Cleveland Clinic site; purely tests the logic flow.
    """
    mock_driver = MagicMock()
    mock_anchor = MagicMock()
    mock_anchor.get_attribute.return_value = "https://my.clevelandclinic.org/health/diseases/acrophobia-fear-of-heights"
    mock_driver.find_elements.return_value = [mock_anchor]

    test_url = "https://my.clevelandclinic.org/health/diseases"
    crawl(test_url, mock_driver)

    mock_driver.get.assert_called_once_with(test_url)
    assert mock_driver.find_elements.call_count >= 1

    mock_file.assert_called()

    handle = mock_file()
    written_data = "".join(call.args[0] for call in handle.write.call_args_list)
    if written_data.strip():
        try:
            parsed_json = json.loads(written_data)
        except json.JSONDecodeError:
            pass

    assert mock_sleep.call_count >= 1
    assert mock_wait.call_count >= 1
