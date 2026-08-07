from typing import Optional

from models.item import Item
from observability.telemetry import traced
from repositories import item_repository
from utils.logger import get_logger

logger = get_logger(__name__)


@traced()
def get_item(item_code: str) -> Optional[Item]:
    """Return an Item by its ERPNext code or a partial item name."""
    if not item_code or not item_code.strip():
        raise ValueError("item_code must not be empty")

    logger.info("Orchestrating Item lookup", extra={"entity": "Item"})
    return item_repository.get_item(item_code)
