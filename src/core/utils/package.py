def create_package_trip(no_vehicles, package_weights, max_weight, max_speed):
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

    # Sort trips based on total weight in descending order
    trips.sort(key=lambda x: sum(x[1]), reverse=True)

    return trips
