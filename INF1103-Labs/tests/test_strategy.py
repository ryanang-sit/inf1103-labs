from main import (
    BulkDiscount,
    NoDiscount,
    Order,
    PercentageDiscount,
    PhysicalProduct,
    StudentDiscount,
    Supplier,
)
import pytest


@pytest.fixture
def sample_order():
    sup = Supplier("S001", "Test Supplier", "test@sup.com")
    prod = PhysicalProduct("P001", "Item", 100.0, 10, sup, 1.0)
    order = Order("ORD-01")
    order.add_order_line(prod, 2)  # Subtotal 200.0
    return order


def test_no_discount(sample_order):
    sample_order.set_discount(NoDiscount())
    assert sample_order.calculate_total() == 200.0


def test_percentage_discount(sample_order):
    sample_order.set_discount(PercentageDiscount(15))
    assert sample_order.calculate_total() == 170.0


def test_bulk_discount(sample_order):
    sample_order.set_discount(BulkDiscount(200.0, 30.0))
    assert sample_order.calculate_total() == 170.0


def test_student_discount(sample_order):
    sample_order.set_discount(StudentDiscount(10))
    assert sample_order.calculate_total() == 180.0