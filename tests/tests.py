import unittest
from src.core.calculator import Calculator
from src.courier_app import CourierApp


class TestCalculatorDeliveryTime(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator(base_delivery_cost=100, rate_distance_cost=10, rate_weight_cost=5)

    def test_total_cost_calculator(self):
        # Without discount
        self.assertEqual(
            self.calculator.total_cost_calculator(distance1_in_km=5, discount_percentage=0, weight1_in_kg=5), 175)
        # With discount
        self.assertEqual(
            self.calculator.total_cost_calculator(distance1_in_km=100, discount_percentage=10, weight1_in_kg=10), 665)

    def test_discount_amount_calculator(self):
        self.calculator.total_cost_before_discount = 700  # Assuming this is set by a previous calculation
        self.assertEqual(self.calculator.discount_amount_calculator(discount_percentage=10), 70)

    def test_calculate_delivery_time(self):
        trips = [
            (['PKG1', 'PKG2'], 125),  # Example trip format: (Package IDs, Max Distance)
            (['PKG3'], 100)
        ]
        packages = [
            ['PKG1', 50, 30, 'OFR001', 0],  # Example package format: ID, Weight, Distance, Coupon, Time placeholder
            ['PKG2', 75, 125, 'OFR008', 0],
            ['PKG3', 175, 100, 'OFR003', 0]
        ]
        max_speed = 70
        expected_delivery_times = [3.98, 1.78, 1.42]  # Example expected times

        results = self.calculator.calculate_delivery_time(trips, packages, max_speed)
        for package, expected_time in zip(results, expected_delivery_times):
            self.assertAlmostEqual(package[-1], expected_time, places=2)


class TestCourierAppIntegration(unittest.TestCase):
    def setUp(self):
        # Assuming there's a way to inject a Calculator and predefined Coupons into the CourierApp for testing
        calculator = Calculator(base_delivery_cost=100, rate_distance_cost=10, rate_weight_cost=5)
        # Mock coupons or preload them as needed
        self.app = CourierApp()

    def test_calculate_delivery_cost(self):
        packages = [
            ['PKG1', 5, 5, 'OFR001'],
            ['PKG2', 15, 5, 'OFR002'],
            ['PKG3', 10, 100, 'OFR003']
        ]
        # Assuming CourierApp has a method to process packages directly for testing
        results = self.app.prompt_delivery_cost()
        self.assertEqual(results, [
            ('PKG1', 0, 175),
            ('PKG2', 0, 275),
            ('PKG3', 35, 665)
        ])

    def test_delivery_time_and_cost_integration(self):
        packages = [
            ['PKG1', 50, 30, 'OFR001'],
            ['PKG2', 75, 125, 'OFR008'],
            ['PKG3', 175, 100, 'OFR003'],
            ['PKG4', 110, 60, 'OFR002'],
            ['PKG5', 155, 95, 'NA']
        ]
        no_of_vehicles = 2
        max_speed = 70
        max_carriable_weight = 200

        results = self.app.prompt_delivery_cost()
        expected_outputs = [
            ('PKG1', 0, 750, 3.98),
            ('PKG2', 0, 1475, 1.78),
            ('PKG3', 0, 2350, 1.42),
            ('PKG4', 105, 1395, 0.85),
            ('PKG5', 0, 2125, 4.19)
        ]
        for result, expected in zip(results, expected_outputs):
            self.assertEqual(result[:-1], expected[:-1])  # Compare ID, discount, and cost
            self.assertAlmostEqual(result[-1], expected[-1], places=2)  # Compare delivery time with rounding


if __name__ == '__main__':
    unittest.main()
