import csv 
from math import sin, cos, acos, radians

def distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface 
    using the Haversine formula.

    Parameters:
    - lat1, lon1: Latitude and longitude of the first point in degrees.
    - lat2, lon2: Latitude and longitude of the second point in degrees.

    Returns:
    - The distance between the two points in kilometers.
    """
    inner_part = min(1.0, max(-1.0, sin(radians(lat1)) * sin(radians(lat2)) + cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(lon1) - radians(lon2))))
    return 6373.0 * acos(inner_part)

# Open and read the CSV file containing road node information
with open("RoadNode.csv", "r") as file:
    csv_reader = csv.reader(file)

    france_locations = []
    germany_locations = []

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Splitting coordinates represented in scientific notation
        x_parts = row[7].split("e")
        y_parts = row[8].split("e")

        # Check if the row corresponds to France or Germany, and if coordinates are valid
        if (row[9] == "France" or row[9] == "Germany") and (len(x_parts) > 1 and len(y_parts) > 1 and x_parts[0] != 'X' and y_parts[0] != 'X'):
            x = float(x_parts[0])
            y = float(y_parts[0])

            # Store the location information in the respective lists
            if row[9] == "France":
                france_locations.append({
                    "name": row[9], 
                    "id":  row[2], 
                    "coords": {"x": x, "y": y}
                })
            if row[9] == "Germany":
                germany_locations.append({
                    "name": row[9], 
                    "id":  row[2], 
                    "coords": {"x": x, "y": y}
                })

    # Calculate the distance between the first locations in France and Germany
    first_route = distance(
        france_locations[0]["coords"]["x"], 
        france_locations[0]["coords"]["y"], 
        germany_locations[0]["coords"]["x"], 
        germany_locations[0]["coords"]["y"]
    )

    # Initialize the most optimal route with the distance and corresponding node IDs
    most_optimal_route = {
        "distance": first_route, 
        "france_id": france_locations[0]["id"], 
        "germany_id": germany_locations[0]["id"]
    } 

    # Iterate through all combinations of France and Germany locations to find the most optimal route
    for fl_index, fl in enumerate(france_locations):
        for gl_index, gl in enumerate(germany_locations):
            current_route = distance(
                france_locations[fl_index]["coords"]["x"], 
                france_locations[fl_index]["coords"]["y"], 
                germany_locations[gl_index]["coords"]["x"], 
                germany_locations[gl_index]["coords"]["y"]
            )

            # Print the comparison between the current route and the most optimal route
            print(f"MOR {most_optimal_route['distance']} & CR {current_route}")

            # Update the most optimal route if the current route is shorter
            if current_route < most_optimal_route["distance"]:
                most_optimal_route = {
                    "distance": current_route, 
                    "france_id": france_locations[fl_index]["id"], 
                    "germany_id": germany_locations[gl_index]["id"]
                }

    # Print the information about the most optimal route
    print("Most optimal route:")
    print(f"Distance: {most_optimal_route['distance']}\nFrance ID: {most_optimal_route['france_id']}\nGermany ID: {most_optimal_route['germany_id']}")
