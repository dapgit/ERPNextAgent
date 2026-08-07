from models.item import Item
from repositories.item_repository import ERPNextItemRepository
from utils.exceptions import ERPNextResourceNotFoundError


class FakeERPNextRESTClient:
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


def test_erpnext_repository_maps_json_to_the_item_domain_model():
    client = FakeERPNextRESTClient(
        doc_by_name={
            "Desk": {
                "item_code": "Desk",
                "item_name": "Office Desk",
                "item_group": "Furniture",
                "stock_uom": "Nos",
            }
        }
    )

    item = ERPNextItemRepository(client=client).get_item("Desk")

    assert item == Item("Desk", "Office Desk", "Furniture", "Nos")


def test_erpnext_repository_falls_back_to_partial_name_match():
    client = FakeERPNextRESTClient(
        doc_by_name={"Desk": {"item_code": "Desk", "item_name": "Office Desk"}},
        list_response={"data": [{"name": "Desk"}]},
    )

    item = ERPNextItemRepository(client=client).get_item("Office")

    assert item.code == "Desk"
    assert item.item_group == "Not set"
    assert item.stock_uom == "Not set"
    assert client.requested_docs == [("Item", "Office"), ("Item", "Desk")]


def test_erpnext_repository_returns_none_when_no_item_matches():
    assert ERPNextItemRepository(client=FakeERPNextRESTClient()).get_item("Unknown") is None
