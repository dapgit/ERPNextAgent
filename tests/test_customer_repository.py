from models.customer import Customer
from repositories.customer_repository import ERPNextCustomerRepository
from utils.exceptions import ERPNextResourceNotFoundError


class FakeERPNextRESTClient:
    """Stands in for ERPNextRESTClient so repository tests never touch the network."""

    def __init__(self, doc_by_name=None, list_response=None):
        self._doc_by_name = doc_by_name or {}
        self._list_response = list_response or {"data": []}
        self.requested_docs = []

    def get_doc(self, doctype, name):
        self.requested_docs.append((doctype, name))
        if name not in self._doc_by_name:
            raise ERPNextResourceNotFoundError(f"No {doctype} named '{name}'")
        return {"data": self._doc_by_name[name]}

    def get_list(self, doctype, fields=None, filters=None):
        return self._list_response


def test_erpnext_repository_maps_json_to_the_customer_domain_model_on_exact_match():
    client = FakeERPNextRESTClient(
        doc_by_name={
            "Grant Plastics Ltd.": {
                "customer_name": "Grant Plastics Ltd.",
                "customer_group": "Demo Customer Group",
                "territory": None,
                "customer_type": "Company",
            }
        }
    )
    repository = ERPNextCustomerRepository(client=client)

    customer = repository.get_customer("Grant Plastics Ltd.")

    assert isinstance(customer, Customer)
    assert customer.name == "Grant Plastics Ltd."
    assert customer.customer_group == "Demo Customer Group"
    assert customer.territory == "Not set"
    assert customer.customer_type == "Company"


def test_erpnext_repository_falls_back_to_partial_match_when_no_exact_match():
    client = FakeERPNextRESTClient(
        doc_by_name={
            "Grant Plastics Ltd.": {
                "customer_name": "Grant Plastics Ltd.",
                "customer_group": "Demo Customer Group",
                "territory": None,
                "customer_type": "Company",
            }
        },
        list_response={"data": [{"name": "Grant Plastics Ltd."}]},
    )
    repository = ERPNextCustomerRepository(client=client)

    customer = repository.get_customer("Grant")

    assert customer.name == "Grant Plastics Ltd."
    assert client.requested_docs == [
        ("Customer", "Grant"),
        ("Customer", "Grant Plastics Ltd."),
    ]


def test_erpnext_repository_returns_none_when_nothing_matches():
    client = FakeERPNextRESTClient()
    repository = ERPNextCustomerRepository(client=client)

    assert repository.get_customer("Nobody") is None
