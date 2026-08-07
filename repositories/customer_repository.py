from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from clients.erpnext_rest_client import ERPNextRESTClient
from models.customer import Customer
from utils.exceptions import ERPNextResourceNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)

NOT_SET = "Not set"


class CustomerRepository(ABC):
    """Contract the Service layer depends on. Implementation is swappable."""

    @abstractmethod
    def get_customer(self, customer_name: str) -> Optional[Customer]:
        raise NotImplementedError


class ERPNextCustomerRepository(CustomerRepository):
    """Retrieves Customer information from a live ERPNext instance."""

    def __init__(self, client: Optional[ERPNextRESTClient] = None):
        self._client = client or ERPNextRESTClient()

    def get_customer(self, customer_name: str) -> Optional[Customer]:
        name = customer_name.strip()
        logger.info(
            "Looking up Customer '%s' in ERPNext", name, extra={"entity": "Customer"}
        )

        try:
            document = self._client.get_doc("Customer", name)
            return self._to_domain(document["data"])
        except ERPNextResourceNotFoundError:
            pass

        match_name = self._find_by_partial_name(name)
        if match_name is None:
            return None

        document = self._client.get_doc("Customer", match_name)
        return self._to_domain(document["data"])

    def _find_by_partial_name(self, customer_name: str) -> Optional[str]:
        listing = self._client.get_list(
            "Customer",
            fields=["name"],
            filters=[["Customer", "customer_name", "like", f"%{customer_name}%"]],
        )
        matches = listing.get("data", [])
        return matches[0]["name"] if matches else None

    @staticmethod
    def _to_domain(data: Dict[str, Any]) -> Customer:
        return Customer(
            name=data.get("customer_name") or data.get("name", ""),
            customer_group=data.get("customer_group") or NOT_SET,
            territory=data.get("territory") or NOT_SET,
            customer_type=data.get("customer_type") or NOT_SET,
        )


def get_customer(customer_name: str) -> Optional[Customer]:
    from repositories.factory import get_customer_repository

    return get_customer_repository().get_customer(customer_name)
