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
    customer = customer_service.get_customer(customer_name)

    if customer is None:
        return f"No customer found with name '{customer_name}'."

    return f"""Customer Name: {customer.name}
Customer Group: {customer.customer_group}
Territory: {customer.territory}
Customer Type: {customer.customer_type}"""
