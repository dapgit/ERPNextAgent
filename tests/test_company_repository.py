import pytest

from models.company import Company
from repositories.company_repository import (
    CompanyRepository,
    ERPNextCompanyRepository,
    MockCompanyRepository,
)


class FakeERPNextRESTClient:
    """Stands in for ERPNextRESTClient so repository tests never touch the network."""

    def __init__(self, doc_by_name=None, list_response=None):
        self._doc_by_name = doc_by_name or {}
        self._list_response = list_response or {"data": []}
        self.requested_docs = []

    def get_doc(self, doctype, name):
        self.requested_docs.append((doctype, name))
        return {"data": self._doc_by_name[name]}

    def get_list(self, doctype, fields=None, filters=None):
        return self._list_response


def test_mock_repository_satisfies_the_abstract_contract():
    assert issubclass(MockCompanyRepository, CompanyRepository)
    assert isinstance(MockCompanyRepository().get_company_information(), Company)


def test_erpnext_repository_maps_json_to_the_company_domain_model():
    client = FakeERPNextRESTClient(
        doc_by_name={
            "A Sports": {
                "name": "A Sports",
                "company_name": "A Sports",
                "country": "India",
                "default_currency": "INR",
            }
        }
    )
    repository = ERPNextCompanyRepository(client=client, company_name="A Sports")

    company = repository.get_company_information()

    assert isinstance(company, Company)
    assert company.name == "A Sports"
    assert company.country == "India"
    assert company.currency == "INR"


def test_erpnext_repository_falls_back_to_first_company_when_unconfigured():
    client = FakeERPNextRESTClient(
        doc_by_name={"A Sports": {"company_name": "A Sports", "country": "India", "default_currency": "INR"}},
        list_response={"data": [{"name": "A Sports"}]},
    )
    repository = ERPNextCompanyRepository(client=client, company_name=None)

    company = repository.get_company_information()

    assert company.name == "A Sports"
    assert client.requested_docs == [("Company", "A Sports")]
