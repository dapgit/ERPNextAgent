import repositories.factory as factory
from repositories.company_repository import ERPNextCompanyRepository
from repositories.customer_repository import ERPNextCustomerRepository
from repositories.item_repository import ERPNextItemRepository


def _reset_factory_cache():
    factory._company_repository = None
    factory._customer_repository = None
    factory._item_repository = None


def test_factory_returns_erpnext_repositories():
    _reset_factory_cache()

    assert isinstance(factory.get_company_repository(), ERPNextCompanyRepository)
    assert isinstance(factory.get_customer_repository(), ERPNextCustomerRepository)
    assert isinstance(factory.get_item_repository(), ERPNextItemRepository)

    _reset_factory_cache()


def test_factory_memoizes_the_repository_instance():
    _reset_factory_cache()

    first = factory.get_company_repository()
    second = factory.get_company_repository()

    assert first is second

    first_item = factory.get_item_repository()
    second_item = factory.get_item_repository()
    assert first_item is second_item

    _reset_factory_cache()
