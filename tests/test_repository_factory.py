import repositories.factory as factory
from repositories.company_repository import ERPNextCompanyRepository, MockCompanyRepository
from repositories.customer_repository import ERPNextCustomerRepository, MockCustomerRepository


def _reset_factory_cache():
    factory._company_repository = None
    factory._customer_repository = None


def test_factory_picks_mock_when_erpnext_url_is_not_configured(monkeypatch):
    _reset_factory_cache()
    monkeypatch.setattr(factory, "get_erpnext_url", lambda: None)

    assert isinstance(factory.get_company_repository(), MockCompanyRepository)
    assert isinstance(factory.get_customer_repository(), MockCustomerRepository)

    _reset_factory_cache()


def test_factory_picks_erpnext_repository_when_url_is_configured(monkeypatch):
    _reset_factory_cache()
    monkeypatch.setattr(factory, "get_erpnext_url", lambda: "http://localhost:8080")

    assert isinstance(factory.get_company_repository(), ERPNextCompanyRepository)
    assert isinstance(factory.get_customer_repository(), ERPNextCustomerRepository)

    _reset_factory_cache()


def test_factory_memoizes_the_repository_instance(monkeypatch):
    _reset_factory_cache()
    monkeypatch.setattr(factory, "get_erpnext_url", lambda: None)

    first = factory.get_company_repository()
    second = factory.get_company_repository()

    assert first is second

    _reset_factory_cache()
