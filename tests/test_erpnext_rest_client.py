import pytest
from conftest import metric_data_points

from clients.erpnext_rest_client import ERPNextRESTClient
from settings import get_erpnext_url
from utils.exceptions import ERPNextError, ERPNextResourceNotFoundError


def test_client_reuses_a_single_session_with_auth_headers_set_once():
    client = ERPNextRESTClient(
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


def test_get_doc_and_get_list_build_expected_resource_paths():
    client = ERPNextRESTClient(base_url="http://localhost:8080", api_key="k", api_secret="s")

    assert client._build_url("/api/resource/Company/A Sports") == (
        "http://localhost:8080/api/resource/Company/A Sports"
    )
    assert client._build_url("/api/resource/Company") == (
        "http://localhost:8080/api/resource/Company"
    )


class _FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self.ok = 200 <= status_code < 400
        self._payload = payload or {}

    def json(self):
        return self._payload


class _FakeSession:
    def __init__(self, response):
        self._response = response
        self.headers = {}

    def get(self, url, params=None, timeout=None):
        return self._response


def test_get_doc_records_a_request_metric_tagged_with_doctype_and_success():
    client = ERPNextRESTClient(base_url="http://localhost:8080", api_key="k", api_secret="s")
    client._session = _FakeSession(_FakeResponse(200, {"data": {"name": "A Sports"}}))

    client.get_doc("Company", "A Sports")

    points = metric_data_points("erpnextagent.erpnext.requests")
    matching = [
        (attrs, value)
        for attrs, value in points
        if attrs.get("doctype") == "Company" and attrs.get("outcome") == "success"
    ]
    assert matching, points
    assert matching[0][1] >= 1


def test_get_doc_records_error_outcome_when_erpnext_returns_not_found():
    client = ERPNextRESTClient(base_url="http://localhost:8080", api_key="k", api_secret="s")
    client._session = _FakeSession(_FakeResponse(404))

    with pytest.raises(ERPNextResourceNotFoundError):
        client.get_doc("Item", "NoSuchItem")

    points = metric_data_points("erpnextagent.erpnext.requests")
    matching = [
        (attrs, value)
        for attrs, value in points
        if attrs.get("doctype") == "Item" and attrs.get("outcome") == "error"
    ]
    assert matching, points
    assert matching[0][1] >= 1


def test_client_can_retrieve_company_information_from_erpnext():
    """
    Independent connectivity check for the ERPNext REST client.

    Talks to ERPNext directly through ERPNextRESTClient only, with no
    Repository or Service layer involved, so that connectivity and
    authentication issues are isolated before those layers are wired up
    (Milestone 5.2).
    """
    if not get_erpnext_url():
        pytest.skip("ERPNEXT_URL is not configured")

    with ERPNextRESTClient() as client:
        try:
            response = client.get_list("Company")
        except ERPNextError as exc:
            pytest.skip(f"ERPNext is not reachable: {exc}")

    assert "data" in response
    assert isinstance(response["data"], list)
    assert len(response["data"]) > 0
    assert "name" in response["data"][0]
