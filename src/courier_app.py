import logging

from src.core.calculator import Calculator
from src.core.coupon import Coupon
from src.core import RATE_DISTANCE_COST, RATE_WEIGHT_COST
from src.core.utils.package import create_package_trip

logger = logging.getLogger(__name__)


class ProcessHandler:

    def __init__(self):
        self.calculator = Calculator(rate_distance_cost=RATE_DISTANCE_COST,
                                     rate_weight_cost=RATE_WEIGHT_COST)

    def process_delivery_time(self, base_delivery_cost, packages, no_vehicles, max_weight, max_speed):
        # this method is to process from input into calculations of trips, delivery_time
        no_vehicles = int(no_vehicles)
        max_speed = int(max_speed)
        max_weight = int(max_weight)

        logger.debug(f'Processing data for calculations of delivery_time')

        trips = create_package_trip(no_vehicles, packages, max_weight, max_speed)
        packages_times = self.calculator.calculate_delivery_time(trips, packages, max_speed)
        packages_costs = self.process_delivery_cost(base_delivery_cost, packages)
        combined_details = []
        logger.debug(f'process delivery cost: {packages_costs} delivery times: {packages_times}')

        # Iterate over both lists simultaneously
        for cost_info in packages_costs:
            for time_info in packages_times:

                if cost_info[0] == time_info[0]:  # Check if the package IDs match
                    combined_details.append([cost_info[0], cost_info[1], cost_info[2], time_info[-1]])

        logger.debug(f'delivery costs and times:  {combined_details}')

        return combined_details

    def process_delivery_cost(self, base_delivery_cost, packages):
        packages_cost = []
        logger.debug(f'Processing for delivery cost and/or time')
        for pkg_id, weight_in_kg, distance_in_km, offer_code, *rest in packages:
            coupon = Coupon.get_coupon(offer_code)
            if coupon and coupon.is_applicable(weight_in_kg, distance_in_km):
                discount_percentage = coupon.discount_percentage
            else:
                discount_percentage = 0

            total_cost = self.calculator.total_cost_calculator(base_delivery_cost, distance_in_km,
                                                               discount_percentage, weight_in_kg)
            discount_amount = self.calculator.discount_amount_calculator(discount_percentage)
            packages_cost.append([pkg_id, discount_amount, total_cost])

        return packages_cost


class CourierApp:
    def __init__(self):
        self.calculator = None
        self.processor = ProcessHandler()
        self.time_and_cost = False
        self.time_only = False

    @staticmethod
    def coupon_creator():
        try:
            coupon_code = input("Enter coupon code (e.g., 'OFR001'): ")
            distance_range = input("Enter distance range (e.g., '0-10'): ")
            weight_range = input("Enter weight range (e.g., '0-50'): ")
            discount_percentage = input("Enter discount percentage (e.g., '10'): ")

            Coupon.create_coupon(coupon_code, distance_range, weight_range, discount_percentage)
            print(f"Coupon {coupon_code} created successfully.")
        except ValueError as e:
            logger.error(f"Invalid discount percentage: {e}")
            print(f"Invalid discount percentage: {e}")
        except Exception as e:
            logger.error(f"An error occurred while creating the coupon: {e}")
            print(f"An error occurred while creating the coupon: {e}")

    def prompt_for_package_details(self):
        """Asks the user for the base delivery cost and the details of each package."""
        try:
            base_delivery_cost, num_packages = map(int, input("Base delivery cost and number of packages: ").split())
            packages_details = [self.prompt_for_single_package() for _ in range(num_packages)]
            print(packages_details)
            return base_delivery_cost, packages_details
        except ValueError as e:
            logger.error(f"Input error: {e}")
            print(f"Please enter valid inputs. Error: {e}")

    @staticmethod
    def prompt_for_single_package():
        """Prompts the user for details of a single package and returns a tuple of the details."""
        while True:
            try:
                pkg_id, weight, distance, offer_code = input(
                    "Enter package details likewise pkg-id, weight_in_kg, distance_in_kmm, coupon_code: PKG1 50 40 "
                    "OFR001: ").split()
                package = [pkg_id, float(weight), float(distance), offer_code]
                return package
            except ValueError as e:
                logger.error(f"Package detail error: {e}")
                print("Please enter valid package details.")

    def io_delivery_cost(self):
        #  this part is input output for calculating delivery costs of the packages
        try:
            logger.debug(f'initiating for calculations of delivery costs')
            base_delivery_cost, packages = self.prompt_for_package_details()

            packages_costs = self.processor.process_delivery_cost(base_delivery_cost, packages)

            if self.time_and_cost:
                print(f'Include time and cost: {self.time_and_cost} packages: {packages}')
                return packages_costs
            else:
                print(f'Include time and cost: {self.time_and_cost} packages: {packages}')
                for pkg_id, discount_amount, total_cost in packages_costs:
                    print(f"{pkg_id} {discount_amount} {total_cost}")
                return packages_costs

        except Exception as error:
            logger.error(f'{error}')
            print(f"Error calculating cost: {error}")

    def io_delivery_time(self):
        logger.debug(f'initiating for calculations of delivery times')

        self.time_and_cost = True
        try:

            base_delivery_cost, packages = self.prompt_for_package_details()
            no_vehicles, max_speed, max_weight = input(
                "Enter no of vehicles, max speed, max weight, likewise: ").split()

            packages = self.processor.process_delivery_time(base_delivery_cost, packages, no_vehicles, max_weight,
                                                            max_speed)

            for package in packages:
                print(package)
                pkg_id = package[0]
                discount_amount = package[6]
                total_cost = package[7]
                delivery_time = package[5]

                print(f"{pkg_id} {int(discount_amount)} {total_cost} {delivery_time}")
            return packages

        except Exception as err:
            print(f'Error in input delivery times: {err}')
            logger.error(f'Error in input delivery times: {err}')

    def run(self):
        logger.debug('Starting app to calculate delivery cost')
        action = input(
            'Enter "1" to calculate delivery cost or "2" to calculate delivery time or "3" to create a coupon:  ')
        if action == "1":
            self.io_delivery_cost()
        elif action == "2":
            self.time_and_cost = True
            self.io_delivery_time()
        elif action == "3":
            self.coupon_creator()

        else:
            print("Invalid selection. Please restart the app and choose either '1' or '2'.")
