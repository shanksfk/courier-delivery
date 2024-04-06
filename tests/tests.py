import unittest
from unittest.mock import patch

from src.core.coupon import Coupon
from src.courier_io import CourierIO
from src.process_handler import ProcessHandler


class PositiveTestCourierAppIntegration(unittest.TestCase):
    def setUp(self):
        self.app = CourierIO()
        self.processor = ProcessHandler()

    def test_calculate_delivery_cost(self):
        packages = [
            ['PKG1', 5, 5, 'OFR001'],
            ['PKG2', 15, 5, 'OFR002'],
            ['PKG3', 10, 100, 'OFR003']
        ]

        base_delivery_cost = 100
        results = self.processor.process_delivery_cost(base_delivery_cost, packages)
        self.assertEqual(results, [
            ['PKG1', 0.0, 175.0],
            ['PKG2', 0.0, 275.0],
            ['PKG3', 35.0, 665.0]
        ])

    def test_delivery_time_and_cost(self):
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
            self.assertEqual(result[:-1], expected[:-1])
            self.assertAlmostEqual(result[-1], expected[-1], places=2)

    def test_brute_force_delivery_time_and_cost(self):

        base_delivery_cost = 100

        packages = [
            ['P1', 99, 100, 'OFR002'],
            ['P2', 199, 100, 'OFR001'],
            ['P3', 199, 100, 'OFR003'],
            ['P4', 1, 100, 'OFR001'],
            ['P5', 1, 100, 'OFR001']
        ]

        no_vehicles = 1
        max_speed = 70
        max_weight = 200

        results = self.processor.process_delivery_time(base_delivery_cost, packages, no_vehicles, max_weight, max_speed)
        print(f'results: {results}')

        expected_outputs = [['P1', 0.0, 1590.0, 1.42],
                            ['P2', 259.0, 2331.0, 4.26],
                            ['P3', 0.0, 2590.0, 7.1],
                            ['P4', 0.0, 610.0, 1.42],
                            ['P5', 0.0, 610.0, 1.42]]
        for result, expected in zip(results, expected_outputs):
            self.assertEqual(result[:-1], expected[:-1])
            self.assertAlmostEqual(result[-1], expected[-1], places=2)

    def test_all_packages_in_one_vehicle(self):
        # this test cramp all packages in one vehicle
        packages = [
            ['PKG1', 50, 30, 'OFR001'],
            ['PKG2', 75, 125, 'OFR002'],
            ['PKG3', 25, 100, 'OFR003']
        ]
        base_delivery_cost = 100
        no_vehicles = 2
        max_speed = 70
        max_weight = 200
        results = self.processor.process_delivery_time(base_delivery_cost, packages, no_vehicles, max_weight, max_speed)
        expected_outputs = [
            ['PKG1', 0.0, 750.0, 0.42],
            ['PKG2', 0.0, 1475.0, 1.78],
            ['PKG3', 42.5, 807.5, 1.42]
        ]
        for result, expected in zip(results, expected_outputs):
            self.assertEqual(result[:-1], expected[:-1])
            self.assertAlmostEqual(result[-1], expected[-1], places=2)

    def test_delivery_time_with_multiple_vehicle_utilization(self):
        # this test gives more vehicles than required in one shot
        packages = [
            ['PKG1', 10, 100, 'OFR001'],  # Lightweight package
            ['PKG2', 190, 100, 'OFR002'],  # Heavy package close to max weight
            ['PKG3', 95, 200, 'OFR003'],
            ['PKG4', 50, 150, 'NA']
        ]
        base_delivery_cost = 100
        no_vehicles = 5  # More vehicles than required in one trip
        max_speed = 70
        max_weight = 200
        results = self.processor.process_delivery_time(base_delivery_cost, packages, no_vehicles, max_weight, max_speed)
        expected_outputs = [

            ['PKG1', 0.0, 700.0, 1.42],
            ['PKG2', 175.0, 2325.0, 1.42],
            ['PKG3', 102.5, 1947.5, 2.85],
            ['PKG4', 0.0, 1350.0, 2.14]
        ]
        for result, expected in zip(results, expected_outputs):
            self.assertEqual(result[:-1], expected[:-1])
            self.assertAlmostEqual(result[-1], expected[-1], places=2)

    def test_valid_coupon_discount_application_with_new_coupon(self):
        # this test creates new coupon and applies it
        new_coupon_name = "TEST001"
        new_coupon_weight_range = "0-10"
        new_coupon_distance_range = "0-100"
        new_coupon_discount_percentage = 10

        Coupon.create_coupon(new_coupon_name, new_coupon_weight_range, new_coupon_distance_range,
                             new_coupon_discount_percentage)

        packages = [['PKG1', 5, 10, new_coupon_name]]
        base_delivery_cost = 100

        results = self.processor.process_delivery_cost(base_delivery_cost, packages)

        expected_results = [['PKG1', 20.0, 180.0]]

        self.assertEqual(results, expected_results)


class NegativeTestCourierAppIntegration(unittest.TestCase):

    def setUp(self):
        self.app = CourierIO()
        self.processor = ProcessHandler()

    def test_invalid_coupon_code(self):
        packages = [['PKG1', 5, 10, 'INVALID']]
        base_delivery_cost = 100
        results = self.processor.process_delivery_cost(base_delivery_cost, packages)
        self.assertEqual(results, [['PKG1', 0.0, 200.0]])


class TestInputValidation(unittest.TestCase):

    @patch('builtins.input', side_effect=['PKG1 -5 -10 OFR001', 'PKG1 5 10 OFR001'])
    def test_negative_then_positive_inputs(self, mocked_input):
        # Test negative attempts, then positive attempt.
        expected_result = ['PKG1', 5.0, 10.0, 'OFR001']
        result = CourierIO().prompt_for_single_package()
        self.assertEqual(result, expected_result)

    @patch('builtins.input', side_effect=['PKG1 five ten OFR001', 'PKG1 5.0 10.0 OFR001'])
    def test_incorrect_data_types_then_correct_input(self, mocked_input):
        # Test that incorrect data types are handled, then a correct attempt follows.
        expected_result = ['PKG1', 5.0, 10.0, 'OFR001']
        result = CourierIO().prompt_for_single_package()
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
