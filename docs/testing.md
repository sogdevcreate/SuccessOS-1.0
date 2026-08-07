# Testing SuccessOS

## Architecture

The suite uses Python's standard `unittest` framework and is organized by test scope:

- `tests/unit/`: isolated core classes and contracts; use fakes or mocks only.
- `tests/integration/`: hand-off between planner, engine, router, handlers, and services.
- `tests/e2e/`: complete deterministic workflows that assert a final observable outcome.
- `tests/regression/`: focused tests retained for known defects.
- `tests/fixtures/`: reusable in-memory dependency fakes.
- `tests/helpers/`: shared test runner and failure-reporting infrastructure.

Existing focused tests at `tests/test_*.py` remain part of the suite for compatibility.

Live Selenium/browser tests should be opt-in and separate from this default deterministic suite. They require an installed driver, network access, and a controlled browser profile. The default browser E2E workflows use `FakeBrowserService` and assert the final title/tab state instead of merely checking that calls were made.

## Writing tests

1. Place a test in the smallest appropriate scope directory.
2. Subclass `ComponentTestCase` for regression-runner diagnostics and set `subsystem`, `component`, and `recommended_location`.
3. Use a fake from `tests.fixtures` or `unittest.mock` for external processes, HTTP, SQLite, Selenium, filesystem boundaries, and GUI interactions.
4. Assert externally visible outcomes: returned result, persisted/recalled data, final browser title/tab state, or service input. Do not only assert that a method executed.

## Running tests

Run the full deterministic suite:

```powershell
python -m unittest discover
```

Run the grouped regression summary:

```powershell
python tests/run_regression.py
```

Generate coverage after installing requirements:

```powershell
python -m coverage run -m unittest discover
python -m coverage html
```

`coverage` is listed in `requirements.txt`; the HTML report is written to `htmlcov/`.
The same commands are executed by `.github/workflows/tests.yml` on pushes and pull requests.

## Debugging failures

The regression runner reports the subsystem, component, test class/method, expected and actual values, exception, stacktrace, and recommended source location. Start at that location, rerun the single test with `python -m unittest <module>.<class>.<method> -v`, and add a focused regression test before changing the implementation.

For live browser failures, capture the normalized URL, action parameters, page title, and a screenshot before inspecting Selenium details. Avoid treating raw webdriver exception text as the diagnosis.
