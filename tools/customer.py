from typing import Dict, Any

CUSTOMERS: Dict[str, Dict[str, Any]] = {
    "abc traders": {
        "name": "ABC Traders",
        "group": "Traders",
        "territory": "Karnataka",
        "type": "Wholesale"
    },
    "anc traders": {
        "name": "ANC Traders",
        "group": "Traders",
        "territory": "Karnataka",
        "type": "Wholesale"
    },
    "xyz stores": {
        "name": "XYZ Stores",
        "group": "Retailers",
        "territory": "Kerala",
        "type": "Retail"
    },
}

_CUSTOMERS = CUSTOMERS


def get_customer(customer_name: str) -> str:
    """
    Return information about an ERPNext customer.

    Args:
        customer_name : The name of the customer to retrieve information for.

    Returns:
        Customer information including 
        customer group,
        territory,
        customer type.
    """
    key = customer_name.lower().strip()
    trader = CUSTOMERS.get(key)
    if not trader:
        for k, v in CUSTOMERS.items():
            if k in key or key in k:
                trader = v
                break

    if not trader:
        return f"No customer found with name '{customer_name}'."

    return f"""Customer Name: {trader['name']}
Customer Group: {trader['group']}
Territory: {trader['territory']}
Customer Type: {trader['type']}"""