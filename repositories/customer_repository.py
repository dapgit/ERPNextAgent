from typing import Dict, Optional

from models.customer import Customer

_CUSTOMERS: Dict[str, Customer] = {
    "abc traders": Customer(
        name="ABC Traders",
        customer_group="Traders",
        territory="Karnataka",
        customer_type="Wholesale",
    ),
    "anc traders": Customer(
        name="ANC Traders",
        customer_group="Traders",
        territory="Karnataka",
        customer_type="Wholesale",
    ),
    "xyz stores": Customer(
        name="XYZ Stores",
        customer_group="Retailers",
        territory="Kerala",
        customer_type="Retail",
    ),
}


def get_customer(customer_name: str) -> Optional[Customer]:
    key = customer_name.lower().strip()

    customer = _CUSTOMERS.get(key)
    if customer:
        return customer

    for k, v in _CUSTOMERS.items():
        if k in key or key in k:
            return v

    return None
