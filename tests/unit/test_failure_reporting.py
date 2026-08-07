from __future__ import annotations

import io
import unittest

from tests.helpers.reporting import ComponentTestCase, FailureReportingRunner


class FailureReportingTests(unittest.TestCase):
    def test_runner_includes_required_failure_context(self) -> None:
        class FailingTest(ComponentTestCase):
            subsystem = "Planner"
            component = "AIPlanner"
            recommended_location = "infrastructure/ai/ai_planner.py"

            def test_failure(self):
                self.assertEqual("actual", "expected")

        stream = io.StringIO()
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(FailingTest)
        result = FailureReportingRunner(stream=stream, verbosity=0).run(suite)
        output = stream.getvalue()

        self.assertFalse(result.wasSuccessful())
        for field in (
            "Subsystem: Planner",
            "Component: AIPlanner",
            "Class: FailingTest",
            "Method: test_failure",
            "Expected: 'expected'",
            "Actual: 'actual'",
            "Exception:",
            "Stacktrace:",
            "Recommended location to inspect: infrastructure/ai/ai_planner.py",
        ):
            with self.subTest(field=field):
                self.assertIn(field, output)
