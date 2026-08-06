import json
from typing import Any, Dict, List, Optional

import requests

from settings import get_erpnext_api_key, get_erpnext_api_secret, get_erpnext_url
from utils.exceptions import (
    ERPNextAuthenticationError,
    ERPNextConnectionError,
    ERPNextResourceNotFoundError,
    ERPNextResponseError,
    ERPNextTimeoutError,
    ERPNextValidationError,
)

DEFAULT_TIMEOUT_SECONDS = 10


class ERPNextRESTClient:
    """
    Thin HTTP client for the ERPNext REST API.

    Owns everything HTTP-shaped: URL construction, authentication headers,
    timeouts, and JSON parsing. Repositories call this client and translate
    the results into domain models; the client itself has no knowledge of
    Customers, Companies, or any other business entity. Named "REST" to
    leave room for a future ERPNextMCPClient sharing the same repository
    contract.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ):
        self._base_url = (base_url or get_erpnext_url() or "").rstrip("/")
        self._timeout = timeout

        api_key = api_key or get_erpnext_api_key()
        api_secret = api_secret or get_erpnext_api_secret()

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"token {api_key}:{api_secret}",
                "Accept": "application/json",
            }
        )

    def get_doc(self, doctype: str, name: str) -> Dict[str, Any]:
        """Fetch a single document, e.g. get_doc("Company", "A Sports")."""
        return self.get(f"/api/resource/{doctype}/{name}")

    def get_list(
        self,
        doctype: str,
        fields: Optional[List[str]] = None,
        filters: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """List documents of a doctype, e.g. get_list("Company")."""
        params: Dict[str, str] = {}
        if fields:
            params["fields"] = json.dumps(fields)
        if filters:
            params["filters"] = json.dumps(filters)

        return self.get(f"/api/resource/{doctype}", params=params or None)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform an authenticated GET request and return the parsed JSON body.

        Args:
            path: API path, e.g. "/api/resource/Customer/ABC Traders".
            params: Optional query string parameters.

        Returns:
            The parsed JSON response body.

        Raises:
            ERPNextConnectionError: The server could not be reached.
            ERPNextTimeoutError: The request exceeded the configured timeout.
            ERPNextAuthenticationError: ERPNext rejected the credentials.
            ERPNextResourceNotFoundError: The document does not exist.
            ERPNextValidationError: ERPNext rejected the request as invalid.
            ERPNextResponseError: Any other error status or invalid JSON.
        """
        url = self._build_url(path)

        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
        except requests.exceptions.Timeout as exc:
            raise ERPNextTimeoutError(f"Timed out calling {url}") from exc
        except requests.exceptions.RequestException as exc:
            raise ERPNextConnectionError(f"Failed to reach {url}: {exc}") from exc

        return self._parse_response(response, url)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "ERPNextRESTClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def _build_url(self, path: str) -> str:
        return f"{self._base_url}/{path.lstrip('/')}"

    def _parse_response(self, response: requests.Response, url: str) -> Dict[str, Any]:
        if response.status_code in (401, 403):
            raise ERPNextAuthenticationError(
                f"ERPNext rejected the request to {url} (status {response.status_code})"
            )

        if response.status_code == 404:
            raise ERPNextResourceNotFoundError(f"No resource found at {url}")

        if response.status_code in (400, 417):
            raise ERPNextValidationError(
                f"ERPNext rejected the request to {url} as invalid (status {response.status_code})"
            )

        if not response.ok:
            raise ERPNextResponseError(
                f"ERPNext returned status {response.status_code} for {url}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise ERPNextResponseError(f"Invalid JSON response from {url}") from exc
