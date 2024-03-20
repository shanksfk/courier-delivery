import math

from src.core.coupon import Coupon
from src.core.utils.package import create_package_trip


class Calculator:

    def __init__(self, base_delivery_cost, rate_distance_cost, rate_weight_cost):
        self.total_cost_before_discount = None
        self.coupon = 'coupon'
        self.base_delivery_cost = base_delivery_cost
        self.rate_distance_cost = rate_distance_cost
        self.rate_weight_cost = rate_weight_cost

    def total_cost_calculator(self, distance1_in_km, discount_percentage, weight1_in_kg):

        distance_cost = self.distance_cost_calculator(distance1_in_km)
        weight_cost = self.weight_cost_calculator(weight1_in_kg)
        self.total_cost_before_discount = self.base_delivery_cost + distance_cost + weight_cost
        discount_amount = self.discount_amount_calculator(discount_percentage)
        total_cost = self.total_cost_before_discount - discount_amount

        return total_cost

    def distance_cost_calculator(self, distance1_in_km):
        distance_cost = distance1_in_km * self.rate_distance_cost

        return distance_cost

    def weight_cost_calculator(self, weight1_in_kg):
        distance_cost = weight1_in_kg * self.rate_weight_cost

        return distance_cost

    def discount_amount_calculator(self, discount_percentage):
        # print(discount_percentage, self.total_cost_before_discount)
        discount_amount = discount_percentage / 100 * self.total_cost_before_discount

        return discount_amount

    def calculate_delivery_time(self, trips, packages, max_speed):
        delivery_times = []
        available_vehicles = 2
        waiting_time_multiplier = 2
        returning_time = []

        for available_vehicle in range(available_vehicles):
            # initiated with zero current time
            returning_time.append(0)

        for trip in trips:

            min_returning_time = min(returning_time)
            # Find the index of the minimum value
            min_index = returning_time.index(min_returning_time)

            # Replace the value at min_index with time_add
            trip_time = max(trip[2])
            multiplied_trip_time = waiting_time_multiplier * trip_time
            returning_time[min_index] = multiplied_trip_time + min_returning_time
            for pkg in trip[0]:
                for package in packages:
                    if pkg == package[0]:
                        # print(pkg, package[0])
                        # delivery_time = int(delivery_time * 100) / 100
                        # print(package[4], min_returning_time)
                        package_delivery_time = min_returning_time + package[4]
                        package_delivery_time = math.ceil(package_delivery_time * 100) / 100
                        package.append(package_delivery_time)

        return packages


