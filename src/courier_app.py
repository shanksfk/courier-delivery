import logging

from src.core.calculator import Calculator
from src.core.coupon import Coupon
from src.core import RATE_DISTANCE_COST, RATE_WEIGHT_COST
from src.core.utils.package import create_package_trip

logger = logging.getLogger(__name__)


class CourierApp:
    def __init__(self):
        self.calculator = None
        self.include_delivery_time = False

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
                    "Enter package details likewise: PKG1 50 40 OFR001: ").split()
                package = [pkg_id, float(weight), float(distance), offer_code]
                return package
            except ValueError as e:
                logger.error(f"Package detail error: {e}")
                print("Please enter valid package details.")

    def prompt_delivery_cost(self):
        try:
            base_delivery_cost, packages_details = self.prompt_for_package_details()
            packages_cost = []
            for pkg_id, weight_in_kg, distance_in_km, offer_code in packages_details:
                coupon = Coupon.get_coupon(offer_code)
                if coupon and coupon.is_applicable(weight_in_kg, distance_in_km):
                    discount_percentage = coupon.discount_percentage
                else:
                    discount_percentage = 0
                self.calculator = Calculator(base_delivery_cost=base_delivery_cost,
                                             rate_distance_cost=RATE_DISTANCE_COST,
                                             rate_weight_cost=RATE_WEIGHT_COST)
                total_cost = self.calculator.total_cost_calculator(distance_in_km,
                                                                   discount_percentage, weight_in_kg)
                discount_amount = self.calculator.discount_amount_calculator(discount_percentage)
                packages_cost.append((pkg_id, total_cost, discount_amount))
                if self.include_delivery_time:
                    return packages_cost
                else:
                    print(f"{pkg_id} {discount_amount} {total_cost}")
        except Exception as error:
            logger.error(f'{error}')
            print(f"Error calculating cost: {error}")

    def prompt_delivery_time(self):
        # try:
        self.include_delivery_time = True
        # packages_cost = self.prompt_delivery_cost()
        base_delivery_cost, packages = self.prompt_for_package_details()
        no_vehicles, max_speed, max_weight = input(
            "Enter no of vehicles, max speed, max carriable weight, likewise: ").split()

        # Convert inputs to the desired data types
        no_vehicles = int(no_vehicles)
        max_speed = int(max_speed)
        max_weight = int(max_weight)
        trips = create_package_trip(no_vehicles, packages, max_weight, max_speed)
        # print(f'trips{trips}')
        self.calculator = Calculator(base_delivery_cost=base_delivery_cost,
                                     rate_distance_cost=RATE_DISTANCE_COST, rate_weight_cost=RATE_WEIGHT_COST)
        package_delivery_times = self.calculator.calculate_delivery_time(trips, packages, max_speed)
        for package in package_delivery_times:
            pkg_id = package[0]
            weight_in_kg = package[1]
            distance_in_km = package[2]
            coupon = Coupon.get_coupon(package[3])
            delivery_time = package[5]
            if coupon and coupon.is_applicable(weight_in_kg, distance_in_km):
                discount_percentage = coupon.discount_percentage
            else:
                discount_percentage = 0
            total_cost = self.calculator.total_cost_calculator(distance_in_km, discount_percentage, weight_in_kg)
            discount_amount = self.calculator.discount_amount_calculator(discount_percentage)

            # package[1] = int(discount_amount)
            # package[2] = total_cost
            # package.pop(3)
            # package.pop(3)
            # package.pop(5)

            print(f"{pkg_id} {int(discount_amount)} {total_cost} {delivery_time}")

        return trips  # Assuming 50 km/h as average speed for delivery
        # except Exception as err:
        #     logger.error(f'{err}')
        #     print(f"Error calculating delivery time: {err}")

    def run(self):
        logger.debug('Starting app to calculate delivery cost')
        action = input(
            'Enter "1" to calculate delivery cost or "2" to calculate delivery time or "3" to create a coupon:  ')
        if action == "1":
            self.prompt_delivery_cost()
        elif action == "2":
            self.include_delivery_time = True
            self.prompt_delivery_time()
        elif action == "3":
            self.coupon_creator()

        else:
            print("Invalid selection. Please restart the app and choose either '1' or '2'.")


