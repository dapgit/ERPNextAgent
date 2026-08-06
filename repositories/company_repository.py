from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from clients.erpnext_rest_client import ERPNextRESTClient
from models.company import Company
from settings import get_erpnext_company_name
from utils.exceptions import ERPNextResourceNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)

NOT_TRACKED_BY_ERPNEXT = "Not tracked on Company in ERPNext"


class CompanyRepository(ABC):
    """Contract the Service layer depends on. Implementation is swappable."""

    @abstractmethod
    def get_company_information(self) -> Company:
        raise NotImplementedError


class MockCompanyRepository(CompanyRepository):
    """In-memory repository used before ERPNext is configured."""

    _COMPANY = Company(
        name="ABC Traders Pvt Ltd",
        country="India",
        currency="INR",
        fiscal_year="2026-2027",
        industry="Distribution",
    )

    def get_company_information(self) -> Company:
        return self._COMPANY


class ERPNextCompanyRepository(CompanyRepository):
    """Retrieves Company information from a live ERPNext instance."""

    def __init__(
        self,
        client: Optional[ERPNextRESTClient] = None,
        company_name: Optional[str] = None,
    ):
        self._client = client or ERPNextRESTClient()
        self._company_name = company_name or get_erpnext_company_name()

    def get_company_information(self) -> Company:
        company_name = self._company_name or self._first_available_company_name()
        logger.info("Fetching Company '%s' from ERPNext", company_name)
        document = self._client.get_doc("Company", company_name)
        return self._to_domain(document["data"])

    def _first_available_company_name(self) -> str:
        listing = self._client.get_list("Company")
        companies = listing.get("data", [])
        if not companies:
            raise ERPNextResourceNotFoundError(
                "No companies are visible to this ERPNext API user"
            )
        return companies[0]["name"]

    @staticmethod
    def _to_domain(data: Dict[str, Any]) -> Company:
        # ERPNext's Company doctype has no fiscal_year or industry field;
        # both live on separate doctypes not yet integrated.
        return Company(
            name=data.get("company_name") or data.get("name", ""),
            country=data.get("country", ""),
            currency=data.get("default_currency", ""),
            fiscal_year=data.get("fiscal_year", NOT_TRACKED_BY_ERPNEXT),
            industry=data.get("industry", NOT_TRACKED_BY_ERPNEXT),
        )


def get_company_information() -> Company:
    from repositories.factory import get_company_repository

    return get_company_repository().get_company_information()
