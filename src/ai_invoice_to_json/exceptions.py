class ExtractionError(Exception):
    """Base exception for all extraction pipeline failures."""

    pass


class ExtractionInputError(ExtractionError):
    """Raised when invalid/non-existent/corrupted input is fed into extraction."""

    pass


class ExtractionValidationError(ExtractionError):
    """Raised when validation failed for an extraction task."""

    pass


class ExtractionAPIError(ExtractionError):
    """Raised when an error is encountered while communicating with LLM API."""

    pass


class ExtractionEvalError(ExtractionError):
    """Raised when an error is encountered while evaluating extraction pipeline."""

    pass


class ExtractionUnexpectedError(ExtractionError):
    """Raised when an unexpected error is encountered during extraction."""

    pass
