import pytest
from src.core.calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator(rate_distance_cost=10, rate_weight_cost=5)

def test_total_cost_no_discount(calculator):
    assert calculator.total_cost_calculator(100, 5, 0, 10) == 150, "Cost calculation without discount failed"

def test_total_cost_with_discount(calculator):
    # Assuming 10% discount on a total cost of 150
    assert calculator.total_cost_calculator(100, 5, 10, 10) == 135, "Cost calculation with discount failed"


import pytest
from src.courier_app import CourierApp
from src.core.calculator import Calculator
from src.core.coupon import Coupon
from unittest.mock import patch

class MockCoupon:
    @staticmethod
    def get_coupon(code):
        if code == "OFR001":
            return Coupon("OFR001", "0-50", "0-200", 10)
        return None

@pytest.fixture
def courier_app():
    app = CourierApp()
    app.calculator = Calculator(rate_distance_cost=10, rate_weight_cost=5)
    return app

@patch('src.core.coupon.Coupon.get_coupon', side_effect=MockCoupon.get_coupon)
def test_calculate_delivery_cost_without_coupon(mock_get_coupon, courier_app):
    # Assuming no discount for the package
    base_delivery_cost = 100
    packages = [("PKG1", 10, 5, "NA")]
    expected = [("PKG1", 150, 0)]
    assert courier_app.prompt_delivery_cost(base_delivery_cost, packages) == expected, "Delivery cost calculation without coupon failed"

@patch('src.core.coupon.Coupon.get_coupon', side_effect=MockCoupon.get_coupon)
def test_calculate_delivery_cost_with_coupon(mock_get_coupon, courier_app):
    # Assuming a discount for the package
    base_delivery_cost = 100
    packages = [("PKG1", 10, 5, "OFR001")]
    expected = [("PKG1", 135, 15)]  # 10% discount on total cost of 150
    assert courier_app.prompt_delivery_cost(base_delivery_cost, packages) == expected, "Delivery cost calculation with coupon failed"
