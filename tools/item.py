from services import item_service


def get_item(item_code: str) -> str:
    """Return ERPNext Item details by item code or partial item name."""
    item = item_service.get_item(item_code)

    if item is None:
        return f"No item found with code or name '{item_code}'."

    return f"""Item Code: {item.code}
Item Name: {item.name}
Item Group: {item.item_group}
Stock UOM: {item.stock_uom}"""
