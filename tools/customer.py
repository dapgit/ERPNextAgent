from services import customer_service


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
    return customer_service.get_customer(customer_name)
