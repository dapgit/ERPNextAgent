"""
Centralizes repository selection: mock vs. ERPNext today, REST vs. MCP later.

Callers only ever see the CompanyRepository / CustomerRepository interface;
which concrete class backs it lives here and nowhere else. Repository
instances are memoized so their underlying ERPNextRESTClient (and its
requests.Session) is reused across calls within the process.

Imports of the concrete repository classes are deferred to call time to
avoid a circular import: each repository module's module-level convenience
function (e.g. company_repository.get_company_information()) calls back
into this factory.
"""
from typing import Optional, TYPE_CHECKING

from settings import get_erpnext_url

if TYPE_CHECKING:
    from repositories.company_repository import CompanyRepository
    from repositories.customer_repository import CustomerRepository

_company_repository: Optional["CompanyRepository"] = None
_customer_repository: Optional["CustomerRepository"] = None


def get_company_repository() -> "CompanyRepository":
    global _company_repository

    if _company_repository is None:
        from repositories.company_repository import (
            ERPNextCompanyRepository,
            MockCompanyRepository,
        )

        _company_repository = (
            ERPNextCompanyRepository() if get_erpnext_url() else MockCompanyRepository()
        )

    return _company_repository


def get_customer_repository() -> "CustomerRepository":
    global _customer_repository

    if _customer_repository is None:
        from repositories.customer_repository import (
            ERPNextCustomerRepository,
            MockCustomerRepository,
        )

        _customer_repository = (
            ERPNextCustomerRepository() if get_erpnext_url() else MockCustomerRepository()
        )

    return _customer_repository
