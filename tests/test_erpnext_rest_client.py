import pytest

from clients.erpnext_client import ERPNextClient
from settings import get_erpnext_url
from utils.exceptions import ERPNextClientError


def test_client_reuses_a_single_session_with_auth_headers_set_once():
    client = ERPNextClient(
        base_url="http://localhost:8080",
        api_key="key",
        api_secret="secret",
    )

    session = client._session
    assert session.headers["Authorization"] == "token key:secret"

    # Building multiple requests must reuse the same session, not recreate it.
    client._build_url("/api/resource/Company")
    client._build_url("/api/resource/Customer")
    assert client._session is session


def test_client_can_retrieve_company_information_from_erpnext():
    """
    Independent connectivity check for the ERPNext client.

    Talks to ERPNext directly through ERPNextClient only, with no Repository
    or Service layer involved, so that connectivity and authentication
    issues are isolated before those layers are wired up (Milestone 5.2).
    """
    if not get_erpnext_url():
        pytest.skip("ERPNEXT_URL is not configured")

    with ERPNextClient() as client:
        try:
            response = client.get("/api/resource/Company")
        except ERPNextClientError as exc:
            pytest.skip(f"ERPNext is not reachable: {exc}")

    assert "data" in response
    assert isinstance(response["data"], list)
    assert len(response["data"]) > 0
    assert "name" in response["data"][0]
