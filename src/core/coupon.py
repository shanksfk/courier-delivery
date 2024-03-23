import json
import logging

logger = logging.getLogger(__name__)

"""
This module is to check coupon validity, and get its amount of discounted, whether its fixed or percentage based

"""

class Coupon:
    """
    This class is to create and manage coupons and apply the correct discount accordingly
    """
    COUPON_FILE = 'src/core/coupons.json'

    def __init__(self, coupon_name, weight_range, distance_range, discount_percentage):
        """
        Initialize a new coupon with the given details

        """
        self.coupon_name = coupon_name
        self.weight_range = weight_range
        self.distance_range = distance_range
        self.discount_percentage = discount_percentage

    @classmethod
    def create_coupon(cls, coupon_name, weight_range, distance_range, discount_percentage):
        """
        Create a new coupon with the given details and save it to the coupons file

        """
        new_coupon = cls(coupon_name, weight_range, distance_range, discount_percentage)
        with open(cls.COUPON_FILE, 'r') as file:
            coupons = json.load(file)
        coupons.append(new_coupon.to_dict())
        with open(cls.COUPON_FILE, 'w') as file:
            json.dump(coupons, file, indent=4)

    @classmethod
    def get_coupon(cls, coupon_name):
        """
        Get the details of a coupon with the given name from the coupons file

        """
        with open(cls.COUPON_FILE, 'r') as file:
            coupons = json.load(file)
        for coupon_data in coupons:
            if coupon_data['coupon_name'] == coupon_name:
                return cls(**coupon_data)
        return None

    def is_valid_for_weight(self, weight_in_kg):
        """
        Check if a given weight is within the valid weight range for this coupon

        """
        # Assuming weight_range is a string like '0-50'
        min_weight, max_weight = map(float, self.weight_range.split('-'))
        # print(min_weight, max_weight)
        return min_weight <= weight_in_kg <= max_weight

    def is_valid_for_distance(self, distance_in_km):
        """
        Check if a given distance is within the valid distance range for this coupon

        """
        # Assuming distance_range is a string like '0-100'
        min_distance, max_distance = map(float, self.distance_range.split('-'))
        # print(min_distance, max_distance)
        return min_distance <= distance_in_km <= max_distance

    def is_applicable(self, weight_in_kg, distance_in_km):
        """
        Check if this coupon is applicable for a given weight and distance

        """
        return self.is_valid_for_weight(weight_in_kg) and self.is_valid_for_distance(distance_in_km)

    def to_dict(self):
        """
        Convert this coupon to a dictionary representation

        """
        return {
            'coupon_name': self.coupon_name,
            'weight_range': self.weight_range,
            'distance_range': self.distance_range,
            'discount_percentage': self.discount_percentage
        }
