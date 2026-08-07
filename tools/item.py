from services import item_service
from utils.logger import get_logger
from utils.tool_execution import execute_tool

logger = get_logger(__name__)


def get_item(item_code: str) -> str:
    """Return ERPNext Item details by item code or partial item name."""
    logger.info("Handling get_item request", extra={"entity": "Item"})

    def _get_item() -> str:
        item = item_service.get_item(item_code)

        if item is None:
            return f"No item found with code or name '{item_code}'."

        return f"""Item Code: {item.code}
Item Name: {item.name}
Item Group: {item.item_group}
Stock UOM: {item.stock_uom}"""

    result = execute_tool(_get_item)
    logger.info("Completed get_item request", extra={"entity": "Item"})
    return result
