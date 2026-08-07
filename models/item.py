from dataclasses import dataclass


@dataclass
class Item:
    """ERPNext Item data required by the assistant."""

    code: str
    name: str
    item_group: str
    stock_uom: str
