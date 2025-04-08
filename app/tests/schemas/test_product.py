from uuid import UUID

from pydantic import ValidationError
import pytest
from tests.factories import product_data
from store.schemas.product import ProductIn


def test_schema_return_sucess():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14 Pro Max"
    assert isinstance(product.id, UUID)


def test_schemas_return_raise():
    data = {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 8500}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 8500},
        "url": "https://errors.pydantic.dev/2.11/v/missing",
    }
