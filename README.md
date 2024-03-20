
Testings:

included in the app are some testcases for testings, to run tests:
    pytest tests.py

# Courier Service App README

## Overview

The Courier Service App is a command-line application designed to calculate the cost and delivery time of courier packages. It allows users to apply discount coupons to their deliveries for more cost-effective shipping options. This app is built using Python and is ideal for logistics and courier companies looking to automate their cost calculation and delivery scheduling processes.

## Features

- Calculate delivery cost for courier packages.
- Calculate delivery time for packages.
- Create and apply discount coupons for deliveries.

## Components

### CourierApp

The main entry point of the application, `CourierApp` handles user interactions and orchestrates the calculation of delivery costs and times. It also supports the creation of discount coupons.

- **Key Methods:**
  - `prompt_delivery_cost()`: Prompts the user for package details and calculates the delivery cost.
  - `prompt_delivery_time()`: Calculates the delivery time based on package details and logistics constraints like vehicle availability.
  - `coupon_creator()`: Allows the creation of discount coupons for use in delivery cost calculations.

### Calculator

Responsible for the core calculations related to delivery cost and time, the `Calculator` class uses delivery parameters and discount information to compute the total cost and expected delivery time for packages.

- **Key Methods:**
  - `total_cost_calculator(distance, discount_percentage, weight)`: Calculates the total cost for delivering a package considering its weight, distance, and any applicable discounts.
  - `calculate_delivery_time(trips, packages, max_speed)`: Estimates the delivery time for packages based on logistics parameters such as trips planning, vehicle speed, and package handling times.

### Coupon

Manages discount coupons, which can be applied to deliveries for reduced costs. Coupons are validated based on package weight and distance criteria.

- **Key Methods:**
  - `create_coupon(coupon_name, weight_range, distance_range, discount_percentage)`: Creates a new coupon with specified criteria for discount application.
  - `get_coupon(coupon_name)`: Retrieves a coupon by its name.
  - `is_applicable(weight, distance)`: Checks if a coupon is applicable to a package based on its weight and delivery distance.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- JSON file `coupons.json` in `src/core` for storing and retrieving coupons

### Installation:

to install the app, clone this repository:
    git clone https://github.com/shanksfk/courier-delivery.git


### Running the App

1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Run the app using the command: `python -m src.main`
4. Follow the on-screen prompts to calculate delivery costs, times, or create coupons.

### Example Usage

- To calculate delivery cost, select option `1` and provide the necessary package details as prompted.
- To calculate delivery time, select option `2` and enter the package and vehicle details as requested.
- To create a new coupon, select option `3` and input the coupon details including code, applicable distance and weight ranges, and the discount percentage.

- Enter base delivery cost and nos of packages
- Enter the package details for each package
- Enter vehicle, max speed, max weight (this is only for delivery time)
- Results

