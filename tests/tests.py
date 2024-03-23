import unittest
from src.core.calculator import Calculator
from src.core.coupon import Coupon
from src.courier_app import CourierApp, ProcessHandler


class TestCourierAppIntegration(unittest.TestCase):
    def setUp(self):
        # Assuming there's a way to inject a Calculator and predefined Coupons into the CourierApp for testing
        # calculator = Calculator(rate_distance_cost=10, rate_weight_cost=5)
        # Mock coupons or preload them as needed
        self.app = CourierApp()
        self.processor = ProcessHandler()

    def test_calculate_delivery_cost(self):
        packages = [
            ['PKG1', 5, 5, 'OFR001'],
            ['PKG2', 15, 5, 'OFR002'],
            ['PKG3', 10, 100, 'OFR003']
        ]

        import os
        import json

        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.dirname(current_directory)
        src_directory = os.path.join(parent_directory, 'src')

        # Specify the path to coupons.json
        Coupon.COUPON_FILE = os.path.join(src_directory, 'core/coupons.json')

        base_delivery_cost = 100
        results = self.processor.process_delivery_cost(base_delivery_cost, packages)
        self.assertEqual(results, [
            ['PKG1', 0.0, 175.0],
            ['PKG2', 0.0, 275.0],
            ['PKG3', 35.0, 665.0]
        ])

    def test_delivery_time_and_cost_integration(self):
        packages = [
            ['PKG1', 50, 30, 'OFR001'],
            ['PKG2', 75, 125, 'OFR008'],
            ['PKG3', 175, 100, 'OFR003'],
            ['PKG4', 110, 60, 'OFR002'],
            ['PKG5', 155, 95, 'NA']
        ]
        base_delivery_cost = 100

        no_vehicles = 2
        max_speed = 70
        max_weight = 200

        results = self.processor.process_delivery_time(base_delivery_cost, packages, no_vehicles, max_weight, max_speed)
        expected_outputs = [
            ['PKG1', 0.0, 750, 3.98],
            ['PKG2', 0.0, 1475, 1.78],
            ['PKG3', 0.0, 2350, 1.42],
            ['PKG4', 105.0, 1395, 0.85],
            ['PKG5', 0.0, 2125, 4.19]
        ]
        for result, expected in zip(results, expected_outputs):
            self.assertEqual(result[:-1], expected[:-1])  # Compare ID, discount, and cost
            self.assertAlmostEqual(result[-1], expected[-1], places=2)  # Compare delivery time with rounding


if __name__ == '__main__':
    unittest.main()
