"""
A subclass of unittest.TestCase which checks for reference leaks.

To use:
- Use testing_refleak.BaseTestCase instead of unittest.TestCase
- Configure and compile Python with --with-pydebug

If sys.gettotalrefcount() is not available (because Python was built without
the Py_DEBUG option), then this module is a no-op and tests will run normally.
"""

from _typeshed import OptExcInfo
from collections.abc import Callable
from typing import TypeVar
from unittest import TestCase as _TestCase, TestResult

_T = TypeVar("_T")

class LocalTestResult(TestResult):
    """A TestResult which forwards events to a parent object, except for Skips."""
    parent_result: TestResult
    def __init__(self, parent_result: TestResult) -> None: ...
    def addError(self, test: _TestCase, error: OptExcInfo) -> None: ...
    def addFailure(self, test: _TestCase, error: OptExcInfo) -> None: ...
    def addSkip(self, test: _TestCase, reason: str) -> None: ...
    def addDuration(self, test: _TestCase, duration: float) -> None: ...

class ReferenceLeakCheckerMixin:
    """A mixin class for TestCase, which checks reference counts."""
    NB_RUNS: int
    def run(self, result: TestResult | None = None) -> TestResult: ...

def SkipReferenceLeakChecker(reason: str) -> Callable[[_T], _T]: ...
def TestCase(test_class: _T) -> _T: ...
