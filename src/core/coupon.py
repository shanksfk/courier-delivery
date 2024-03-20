import json
import logging

logger = logging.getLogger(__name__)

'''
This module is to check coupon validity, and get its amount of discounted, whether its fixed or percentage based

'''


class Coupon:
    COUPON_FILE = 'src/core/coupons.json'

    def __init__(self, coupon_name, weight_range, distance_range, discount_percentage):
        self.coupon_name = coupon_name
        self.weight_range = weight_range
        self.distance_range = distance_range
        self.discount_percentage = discount_percentage

    @classmethod
    def create_coupon(cls, coupon_name, weight_range, distance_range, discount_percentage):
        new_coupon = cls(coupon_name, weight_range, distance_range, discount_percentage)
        with open(cls.COUPON_FILE, 'r') as file:
            coupons = json.load(file)
        coupons.append(new_coupon.to_dict())
        with open(cls.COUPON_FILE, 'w') as file:
            json.dump(coupons, file, indent=4)

    @classmethod
    def get_coupon(cls, coupon_name):
        with open(cls.COUPON_FILE, 'r') as file:
            coupons = json.load(file)
        for coupon_data in coupons:
            if coupon_data['coupon_name'] == coupon_name:
                return cls(**coupon_data)
        return None

    def is_valid_for_weight(self, weight_in_kg):
        # Assuming weight_range is a string like '0-50'
        min_weight, max_weight = map(float, self.weight_range.split('-'))
        # print(min_weight, max_weight)
        return min_weight <= weight_in_kg <= max_weight

    def is_valid_for_distance(self, distance_in_km):
        # Assuming distance_range is a string like '0-100'
        min_distance, max_distance = map(float, self.distance_range.split('-'))
        # print(min_distance, max_distance)
        return min_distance <= distance_in_km <= max_distance

    def is_applicable(self, weight_in_kg, distance_in_km):
        return self.is_valid_for_weight(weight_in_kg) and self.is_valid_for_distance(distance_in_km)

    def to_dict(self):
        return {
            'coupon_name': self.coupon_name,
            'weight_range': self.weight_range,
            'distance_range': self.distance_range,
            'discount_percentage': self.discount_percentage
        }

