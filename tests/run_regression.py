"""Run SuccessOS regression groups with component-aware diagnostics."""

from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tests.helpers.reporting import FailureReportingRunner


SUBSYSTEMS = {
    "Planner": ("tests.test_ai_planner", "tests.regression.test_browser_intents"),
    "Browser": ("tests.test_browser_policy_manager", "tests.e2e.test_workflows.BrowserWorkflowTests"),
    "Filesystem": ("tests.test_filesystem_sandbox", "tests.e2e.test_workflows.FilesystemWorkflowTests"),
    "Memory": ("tests.integration.test_execution_pipeline", "tests.e2e.test_workflows.MemoryWorkflowTests"),
    "Authorization": ("tests.test_permission_manager", "tests.e2e.test_workflows.SafetyWorkflowTests"),
    "Execution": ("tests.unit.test_core",),
}


def main() -> int:
    print("====================================")
    print("SuccessOS Regression Suite")
    print("====================================")

    loader = unittest.defaultTestLoader
    passed = 0
    failed = 0

    for subsystem, test_names in SUBSYSTEMS.items():
        suite = unittest.TestSuite(
            loader.loadTestsFromName(name)
            for name in test_names
        )
        stream = io.StringIO()
        result = FailureReportingRunner(stream=stream, verbosity=0).run(suite)
        status = "PASS" if result.wasSuccessful() else "FAIL"
        print(f"{subsystem:<15} {status}")

        if result.wasSuccessful():
            passed += result.testsRun
        else:
            failed += len(result.failures) + len(result.errors)
            print(stream.getvalue().strip())

    print("\nTotal:", passed + failed)
    print("Passed:", passed)
    print("Failed:", failed)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
