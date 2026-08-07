"""Context-rich test reporting used by the regression runner."""

from __future__ import annotations

import traceback
import unittest


class ComponentTestCase(unittest.TestCase):
    """Base test case that identifies the owning subsystem on failure."""

    subsystem = "General"
    component = "Unspecified"
    recommended_location = "Inspect the test and its direct dependencies."

    def assertEqual(self, first, second, msg=None) -> None:
        self.expected = repr(second)
        self.actual = repr(first)
        super().assertEqual(first, second, msg)

    def assertTrue(self, expr, msg=None) -> None:
        self.expected = "True"
        self.actual = repr(expr)
        super().assertTrue(expr, msg)

    def assertFalse(self, expr, msg=None) -> None:
        self.expected = "False"
        self.actual = repr(expr)
        super().assertFalse(expr, msg)

    def assertIn(self, member, container, msg=None) -> None:
        self.expected = f"{member!r} is present"
        self.actual = repr(container)
        super().assertIn(member, container, msg)


class FailureReportingResult(unittest.TextTestResult):
    """Render failures with diagnostics suitable for local debugging and CI."""

    def addFailure(self, test, err) -> None:
        super().addFailure(test, err)
        self._write_context(test, err, "Assertion failure")

    def addError(self, test, err) -> None:
        super().addError(test, err)
        self._write_context(test, err, "Unexpected exception")

    def _write_context(self, test, err, category: str) -> None:
        exception = err[1]
        stacktrace = "".join(traceback.format_exception(*err))
        expected = getattr(test, "expected", "Documented assertion outcome")
        actual = getattr(test, "actual", str(exception))

        self.stream.writeln("\n------------------------------------")
        self.stream.writeln(f"Subsystem: {getattr(test, 'subsystem', 'General')}")
        self.stream.writeln(f"Component: {getattr(test, 'component', 'Unspecified')}")
        self.stream.writeln(f"Class: {test.__class__.__name__}")
        self.stream.writeln(f"Method: {test._testMethodName}")
        self.stream.writeln(f"Expected: {expected}")
        self.stream.writeln(f"Actual: {actual}")
        self.stream.writeln(f"Exception: {category}: {exception}")
        self.stream.writeln("Stacktrace:")
        self.stream.writeln(stacktrace.rstrip())
        self.stream.writeln(
            "Recommended location to inspect: "
            f"{getattr(test, 'recommended_location', 'the failing component')}"
        )


class FailureReportingRunner(unittest.TextTestRunner):
    """Test runner that installs :class:`FailureReportingResult`."""

    resultclass = FailureReportingResult
