from main import DigitalProduct, PhysicalProduct, ProductFactory, Supplier
import pytest


def test_factory_create_physical():
    sup = Supplier("S001", "Sup", "sup@test.com")
    prod = ProductFactory.create("physical", "P10", "Desk", 50.0, 5, sup, 2.5)
    assert isinstance(prod, PhysicalProduct)
    assert prod.get_id() == "P10"
    assert prod.get_weight() == 2.5


def test_factory_create_digital():
    sup = Supplier("S001", "Sup", "sup@test.com")
    prod = ProductFactory.create(
        "digital", "D10", "App", 20.0, 100, sup, 50.0
    )
    assert isinstance(prod, DigitalProduct)
    assert prod.get_download_size() == 50.0


def test_factory_unknown_type():
    sup = Supplier("S001", "Sup", "sup@test.com")
    with pytest.raises(ValueError, match="Unknown product type"):
        ProductFactory.create("service", "S10", "Install", 100.0, 1, sup, 5.0)