class ERPNextError(Exception):
    """Base exception for all ERPNext integration errors."""


class ERPNextConnectionError(ERPNextError):
    """Raised when the ERPNext server cannot be reached (network failure)."""


class ERPNextTimeoutError(ERPNextError):
    """Raised when a request to ERPNext exceeds the configured timeout."""


class ERPNextAuthenticationError(ERPNextError):
    """Raised when ERPNext rejects the supplied API credentials (401/403)."""


class ERPNextResourceNotFoundError(ERPNextError):
    """Raised when the requested document does not exist in ERPNext (404)."""


class ERPNextValidationError(ERPNextError):
    """Raised when ERPNext rejects the request as invalid (400/417)."""


class ERPNextResponseError(ERPNextError):
    """Raised for any other error status or an unparsable response body."""
