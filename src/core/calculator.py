import math


class CostCalculator:

    def __init__(self, rate_distance_cost, rate_weight_cost):
        """
        Initializes the Calculator class.
         """
        self.total_cost_before_discount = None
        self.rate_distance_cost = rate_distance_cost
        self.rate_weight_cost = rate_weight_cost

    def total_cost_before_calculator(self, base_delivery_cost, distance1_in_km, weight1_in_kg):
        """
        Calculates the total cost of a delivery, including distance, weight, and base cost.
        """
        distance_cost = DistanceCalculator.distance_cost_calculator(self.rate_distance_cost, distance1_in_km)
        weight_cost = WeightCalculator.weight_cost_calculator(self.rate_weight_cost, weight1_in_kg)
        self.total_cost_before_discount = base_delivery_cost + distance_cost + weight_cost

        return self.total_cost_before_discount

    def total_cost_after_discount(self, discount_amount):

        return self.total_cost_before_discount - discount_amount


class DiscountCalculator:
    @staticmethod
    def calculate_discount_amount(total_cost_before_discount, discount_percentage):
        """
        Calculates the discount amount for a delivery.
        """
        discount_percentage = float(discount_percentage)
        discount_amount = float('{:.1f}'.format(discount_percentage / 100 * total_cost_before_discount))
        return discount_amount


class WeightCalculator:
    @staticmethod
    def weight_cost_calculator(rate_weight_cost, weight1_in_kg):
        """
        Calculates the cost of weight for a delivery.
        """
        distance_cost = weight1_in_kg * rate_weight_cost

        return distance_cost


class DistanceCalculator:
    @staticmethod
    def distance_cost_calculator(rate_distance_cost, distance1_in_km):
        """
        Calculates the cost of distance for a delivery.
        """
        distance_cost = distance1_in_km * rate_distance_cost

        return distance_cost


class TimeCalculator:

    @staticmethod
    def create_package_trip(package_weights, max_weight, max_speed):
        # Sort packages based on their weights
        sorted_packages = sorted(package_weights, key=lambda x: x[1], reverse=True)

        trips = []
        current_trip = [[], [], []]
        current_weight = 0
        for package in package_weights:
            distance = package[2]
            delivery_time = distance / max_speed
            delivery_time = int(delivery_time * 100) / 100
            package.append(delivery_time)
            # print(package)

        for package in sorted_packages:

            if current_weight + package[1] <= max_weight:

                current_trip[0].append(package[0])  # Add package name to current trip
                current_trip[1].append(package[1])  # Add package weight to current trip
                current_trip[2].append(package[4])  # Add package delivery time to current trip
                current_weight += package[1]  # Update current weight

            else:

                trips.append(current_trip)  # Add current trip to trips list
                current_trip = [[package[0]], [package[1]], [package[4]]]  # Start a new trip
                current_weight = package[1]  # Reset current weight

        if current_trip != [[], [], []]:
            trips.append(current_trip)  # Add the last trip if not empty

        # Sort trips based on no's of  package in descending order
        trips = sorted_trips = sorted(trips, key=lambda trip: len(trip[0]), reverse=True)

        return trips

    @staticmethod
    def calculate_delivery_time(available_vehicles, trips, packages):
        """
        Calculates the delivery time for a set of packages.
        """
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
                        package_delivery_time = min_returning_time + package[4]
                        package_delivery_time = math.ceil(package_delivery_time * 100) / 100
                        package.append(package_delivery_time)

        return packages
