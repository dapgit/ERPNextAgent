class ERPNextClientError(Exception):
    """Base exception for all ERPNext client errors."""


class ERPNextConnectionError(ERPNextClientError):
    """Raised when the ERPNext server cannot be reached (network failure, timeout)."""


class ERPNextAuthenticationError(ERPNextClientError):
    """Raised when ERPNext rejects the supplied API credentials."""


class ERPNextResponseError(ERPNextClientError):
    """Raised when ERPNext returns an error status or an unparsable response."""
