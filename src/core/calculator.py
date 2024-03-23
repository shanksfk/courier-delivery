import math


class Calculator:

    def __init__(self, rate_distance_cost, rate_weight_cost):
        """
        Initializes the Calculator class.
        Args:
            rate_distance_cost (float): The rate that is being charged for each kilometer of distance.
            rate_weight_cost (float): The rate that is being charged for each kilogram of weight.
        """
        self.total_cost_before_discount = None
        self.coupon = 'coupon'
        self.rate_distance_cost = rate_distance_cost
        self.rate_weight_cost = rate_weight_cost

    def total_cost_calculator(self, base_delivery_cost, distance1_in_km, discount_percentage, weight1_in_kg):
        """
        Calculates the total cost of a delivery, including distance, weight, and base cost.
        Args:
            base_delivery_cost (float): The base cost of the delivery.
            distance1_in_km (float): The distance of the delivery, in kilometers.
            discount_percentage (float): The discount percentage that is being applied to the delivery.
            weight1_in_kg (float): The weight of the delivery, in kilograms.
        Returns:
            float: The total cost of the delivery, after any discounts are applied.
        """
        distance_cost = self.distance_cost_calculator(distance1_in_km)
        weight_cost = self.weight_cost_calculator(weight1_in_kg)
        self.total_cost_before_discount = base_delivery_cost + distance_cost + weight_cost
        discount_amount = self.discount_amount_calculator(discount_percentage)
        total_cost = self.total_cost_before_discount - discount_amount

        return total_cost

    def distance_cost_calculator(self, distance1_in_km):
        """
        Calculates the cost of distance for a delivery.
        Args:
            distance1_in_km (float): The distance of the delivery, in kilometers.
        Returns:
            float: The cost of distance for the delivery.
        """
        distance_cost = distance1_in_km * self.rate_distance_cost

        return distance_cost

    def weight_cost_calculator(self, weight1_in_kg):
        """
        Calculates the cost of weight for a delivery.
        Args:
            weight1_in_kg (float): The weight of the delivery, in kilograms.
        Returns:
            float: The cost of weight for the delivery.
        """
        distance_cost = weight1_in_kg * self.rate_weight_cost

        return distance_cost

    def discount_amount_calculator(self, discount_percentage):
        """
        Calculates the discount amount for a delivery.
        Args:
            discount_percentage (float): The discount percentage that is being applied to the delivery.
        Returns:
            float: The discount amount for the delivery.
        """
        # print(discount_percentage, self.total_cost_before_discount)
        discount_amount = float('{:.1f}'.format(discount_percentage / 100 * self.total_cost_before_discount))

        return discount_amount

    def calculate_delivery_time(self, trips, packages, max_speed):
        """
        Calculates the delivery time for a set of packages.
        Args:
            trips (list): A list of trips, where each trip is a list of packages.
            packages (list): A list of packages, where each package is a list of information.
            max_speed (float): The maximum speed of the vehicles that are being used for the delivery.
        Returns:
            list: A list of packages, where each package has an additional field indicating the delivery time.
        """
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
