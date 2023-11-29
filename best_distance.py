import csv 
from math import sin, cos, acos, radians


def distance(lat1, lon1, lat2, lon2):
    inner_part = min(1.0, max(-1.0, sin(radians(lat1)) * sin(radians(lat2)) + cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(lon1) - radians(lon2))))
    return 6373.0 * acos(inner_part)


with open("RoadNode.csv", "r") as node_file:
    with open("RoadLink.csv", "r") as link_file: 
        csv_road_node = list(csv.reader(node_file))[1:]
        csv_road_link = list(csv.reader(link_file))[1:]

        from_to_nodes = []
        for row_index, row in enumerate(csv_road_link):
            fuel_integer = int(row[3].split(";")[-1])
            fuel_decimal = int(row[4].split(";")[0])
            fuel_price = float(f"{fuel_integer}.{fuel_decimal}")


            row = row[0].split(";")
            if row[5] == "France" or row[5] == "Germany":

                from_to_nodes.append({
                    "id": int(row[0]),
                    "from_node": int(row[3]),
                    "to_node": int(row[4]),
                    "fuel_price": fuel_price
                })


        fastest_route = { 
            "id": "", 
            "distance_fuel": 100000 
        }


        for ft_node in from_to_nodes:
            coords_from = { "x": 0.0, "y": 0.0 }
            coords_to = { "x": 0.0, "y": 0.0 }

            for road in csv_road_node:
                road_id = int(road[2])
                
                if len(road[7]) > 1 and len(road[8]) > 1 and road[7] != "X" and road[8] != "Y" and road[7] != "0.0" and road[8] != "0.0":
                    if road_id == ft_node["from_node"]:
                        x = float(road[7].split("e")[0])
                        y = float(road[8].split("e")[0])
                        coords_from = { "x": x, "y": y }

                    if road_id == ft_node["to_node"]:
                        x = float(road[7].split("e")[0])
                        y = float(road[8].split("e")[0])
                        coords_to = { "x": x, "y": y }
 
            current_distance = distance(
                coords_from["x"],
                coords_from["y"],
                coords_to["x"],
                coords_to["y"],
            )
            current_distance_fuel = (current_distance + ft_node["fuel_price"]) / 2


            print(f"Fastest distance {fastest_route['distance_fuel']}")
            print(f"Current distance: {current_distance_fuel}")

            if current_distance_fuel < fastest_route["distance_fuel"] and current_distance_fuel != 0.0:
                fastest_route["id"] = ft_node["id"]
                fastest_route["distance_fuel"] = current_distance_fuel


        print(f"""\nFastest way: 
            \nID: {fastest_route["id"]} 
            \nDistance: {fastest_route["distance_fuel"]}
        """)

