from observability.telemetry import get_tracer
from services import customer_service
from utils.logger import get_logger
from utils.tool_execution import execute_tool

logger = get_logger(__name__)
tracer = get_tracer(__name__)


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
    logger.info("Handling get_customer request", extra={"entity": "Customer"})

    def _get_customer() -> str:
        with tracer.start_as_current_span("tools.customer.get_customer"):
            customer = customer_service.get_customer(customer_name)

            if customer is None:
                return f"No customer found with name '{customer_name}'."

            return f"""Customer Name: {customer.name}
Customer Group: {customer.customer_group}
Territory: {customer.territory}
Customer Type: {customer.customer_type}"""

    result = execute_tool(_get_customer)
    logger.info("Completed get_customer request", extra={"entity": "Customer"})
    return result
