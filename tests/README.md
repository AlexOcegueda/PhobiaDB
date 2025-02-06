# PhobiaDB Testing Overview

This project uses **pytest** for automated testing. Our tests are located in the `tests/` folder:

- **`test_api.py`**:  
  - Tests our Flask API endpoints with the Flask test client.  
  - Ensures routes like `/phobia/<name>` or `/symptoms/<name>` return correct data or HTML.

- **`test_ccs.py`**:  
  - Contains **unit tests** for our crawler (`process_disease_page` logic) by providing sample HTML to parse.  
  - Also includes a **mocked Selenium** test (`test_crawl_click_letters`) verifying that the crawler calls the browser driver, writes JSON, etc. 
  - This does **not** hit the real Cleveland Clinic site — it’s purely a mock test.

- **`test_integration_live.py`**:
  - **Integration tests** that call the **live** endpoints (e.g. `treatments/Arachnophobia` on PythonAnywhere).  
  - This confirms the deployed site works as expected, checking status codes and returned data.

## Running Tests

1. Install dependencies: `pip install -r requirements.txt`  
2. Run all tests with `pytest`.  
3. If you want to skip integration tests, you can either remove the `@pytest.mark.integration` or tell pytest to skip them with `pytest -m "not integration"` (after you define the marker in `pytest.ini`).

## Known Markers

```
pytest -m integration    # only integration tests
pytest -m "not integration"   # skip integration tests
```
