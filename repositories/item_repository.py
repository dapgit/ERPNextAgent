from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from clients.erpnext_rest_client import ERPNextRESTClient
from models.item import Item
from utils.exceptions import ERPNextResourceNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)

NOT_SET = "Not set"


class ItemRepository(ABC):
    """Contract for retrieving Item domain models."""

    @abstractmethod
    def get_item(self, item_code: str) -> Optional[Item]:
        raise NotImplementedError


class ERPNextItemRepository(ItemRepository):
    """Retrieves Item information from a live ERPNext instance."""

    def __init__(self, client: Optional[ERPNextRESTClient] = None):
        self._client = client or ERPNextRESTClient()

    def get_item(self, item_code: str) -> Optional[Item]:
        code = item_code.strip()
        logger.info("Looking up Item '%s' in ERPNext", code)

        try:
            document = self._client.get_doc("Item", code)
            return self._to_domain(document["data"])
        except ERPNextResourceNotFoundError:
            pass

        match_code = self._find_by_partial_name(code)
        if match_code is None:
            return None

        document = self._client.get_doc("Item", match_code)
        return self._to_domain(document["data"])

    def _find_by_partial_name(self, item_name: str) -> Optional[str]:
        listing = self._client.get_list(
            "Item",
            fields=["name"],
            filters=[["Item", "item_name", "like", f"%{item_name}%"]],
        )
        matches = listing.get("data", [])
        return matches[0]["name"] if matches else None

    @staticmethod
    def _to_domain(data: Dict[str, Any]) -> Item:
        return Item(
            code=data.get("item_code") or data.get("name", ""),
            name=data.get("item_name") or data.get("name", ""),
            item_group=data.get("item_group") or NOT_SET,
            stock_uom=data.get("stock_uom") or NOT_SET,
        )


def get_item(item_code: str) -> Optional[Item]:
    from repositories.factory import get_item_repository

    return get_item_repository().get_item(item_code)
