import logging
from src.core import RATE_DISTANCE_COST, RATE_WEIGHT_COST
from src.core.calculator import CostCalculator, DistanceCalculator, TimeCalculator
from src.core.coupon import Coupon

logger = logging.getLogger(__name__)


class ProcessHandler:

    def __init__(self):
        self.cost_calculator = CostCalculator(rate_distance_cost=RATE_DISTANCE_COST,
                                              rate_weight_cost=RATE_WEIGHT_COST)

    def process_delivery_time(self, base_delivery_cost, packages, no_vehicles, max_weight, max_speed):
        # this method is to process from input into calculations of trips, delivery_time
        no_vehicles = int(no_vehicles)
        max_speed = int(max_speed)
        max_weight = int(max_weight)
        try:
            logger.debug(f'Processing data for calculations of delivery_time')

            trips = TimeCalculator.create_package_trip(packages, max_weight, max_speed)
            # print(f'trips: {trips}')
            logger.debug(f'Trips: {trips}')
            packages_times = TimeCalculator.calculate_delivery_time(no_vehicles, trips, packages)
            # print(f'packages times: {packages_times}')

            packages_costs = self.process_delivery_cost(base_delivery_cost, packages)
            # print(f'packages cost: {packages_costs}')
            combined_details = []
            logger.debug(f'process delivery cost: {packages_costs} delivery times: {packages_times}')

            # Iterate over both lists simultaneously
            for cost_info in packages_costs:
                for time_info in packages_times:

                    if cost_info[0] == time_info[0]:  # Check if the package IDs match
                        combined_details.append([cost_info[0], cost_info[1], cost_info[2], time_info[-1]])

            logger.debug(f'delivery costs and times:  {combined_details}')
            return combined_details

        except Exception as err:
            logger.debug(f' error processing for delivery costs adn time: {err}')

    def process_delivery_cost(self, base_delivery_cost, packages):
        packages_cost = []
        try:
            logger.debug(f'Processing for delivery cost and/or time')
            for pkg_id, weight_in_kg, distance_in_km, offer_code, *rest in packages:
                coupon = Coupon.get_coupon(offer_code)
                if coupon and coupon.is_applicable(weight_in_kg, distance_in_km):
                    discount_percentage = coupon.discount_percentage
                else:
                    discount_percentage = 0
                total_cost = self.cost_calculator.total_cost_calculator(base_delivery_cost, distance_in_km,
                                                                        discount_percentage, weight_in_kg)
                discount_amount = self.cost_calculator.discount_amount_calculator(discount_percentage)
                packages_cost.append([pkg_id, discount_amount, total_cost])

            return packages_cost

        except Exception as err:
            print(f'error processing for delivery costs: {err}')
            logger.debug(f' error processing for delivery costs: {err}', exc_info=True)
