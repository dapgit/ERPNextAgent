from typing import Any, Dict, Optional

import requests

from settings import get_erpnext_api_key, get_erpnext_api_secret, get_erpnext_url
from utils.exceptions import (
    ERPNextAuthenticationError,
    ERPNextConnectionError,
    ERPNextResponseError,
)

DEFAULT_TIMEOUT_SECONDS = 10


class ERPNextClient:
    """
    Thin HTTP client for the ERPNext REST API.

    Owns everything HTTP-shaped: URL construction, authentication headers,
    timeouts, and JSON parsing. Repositories call this client and translate
    the results into domain models; the client itself has no knowledge of
    Customers, Companies, or any other business entity.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
    ):
        self._base_url = (base_url or get_erpnext_url() or "").rstrip("/")
        self._api_key = api_key or get_erpnext_api_key()
        self._api_secret = api_secret or get_erpnext_api_secret()
        self._timeout = timeout

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform an authenticated GET request and return the parsed JSON body.

        Args:
            path: API path, e.g. "/api/resource/Customer/ABC Traders".
            params: Optional query string parameters.

        Returns:
            The parsed JSON response body.

        Raises:
            ERPNextConnectionError: The server could not be reached or timed out.
            ERPNextAuthenticationError: ERPNext rejected the credentials.
            ERPNextResponseError: ERPNext returned an error status or invalid JSON.
        """
        url = self._build_url(path)

        try:
            response = requests.get(
                url,
                headers=self._auth_headers(),
                params=params,
                timeout=self._timeout,
            )
        except requests.exceptions.Timeout as exc:
            raise ERPNextConnectionError(f"Timed out calling {url}") from exc
        except requests.exceptions.RequestException as exc:
            raise ERPNextConnectionError(f"Failed to reach {url}: {exc}") from exc

        return self._parse_response(response, url)

    def _build_url(self, path: str) -> str:
        return f"{self._base_url}/{path.lstrip('/')}"

    def _auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"token {self._api_key}:{self._api_secret}",
            "Accept": "application/json",
        }

    def _parse_response(self, response: requests.Response, url: str) -> Dict[str, Any]:
        if response.status_code in (401, 403):
            raise ERPNextAuthenticationError(
                f"ERPNext rejected the request to {url} (status {response.status_code})"
            )

        if not response.ok:
            raise ERPNextResponseError(
                f"ERPNext returned status {response.status_code} for {url}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise ERPNextResponseError(f"Invalid JSON response from {url}") from exc
