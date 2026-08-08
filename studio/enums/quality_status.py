from enum import Enum


class QualityStatus(str, Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    RETRY_EXHAUSTED = "retry_exhausted"
