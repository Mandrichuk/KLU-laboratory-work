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
            row = row[0].split(";")
            if row[5] == "France" or row[5] == "Germany":
                from_to_nodes.append({
                    "id": int(row[0]),
                    "from_node": int(row[3]),
                    "to_node": int(row[4])
                })

        fastest_route = { "id": "", "distance": 100000 }


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
 
            current_route = distance(
                coords_from["x"],
                coords_from["y"],
                coords_to["x"],
                coords_to["y"],
            )

            print("current: " + str(current_route))
            print("fastest: " + str(fastest_route))
            if current_route < fastest_route["distance"] and current_route != 0.0:
                fastest_route["id"] = ft_node["id"]
                fastest_route["distance"] = current_route



        print(f"""
              Fastest Route:\n
              ID: {fastest_route["id"]}\n
              Distance: {fastest_route["distance"]}\n
        """)