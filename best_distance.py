import csv 
from math import sin, cos, acos, radians


def distance(lat1, lon1, lat2, lon2):
    inner_part = min(1.0, max(-1.0, sin(radians(lat1)) * sin(radians(lat2)) + cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(lon1) - radians(lon2))))
    return 6373.0 * acos(inner_part)


with open("RoadNode.csv", "r") as node_file:
    csv_road_node = csv.reader(node_file)
    with open("RoadLink.csv", "r") as link_file: 
        csv_road_link = csv.reader(link_file)

        from_to_nodes = []
        for row_index, row in enumerate(list(csv_road_link)[1:4]):
            row = row[0].split(";")
            from_to_nodes.append({
                "obj_id": int(row[0]),
                "from_node": int(row[3]),
                "to_node": int(row[4])
            })




        fastest_destination = {
            "obj_id": from_to_nodes[0]["obj_id"], 
            "distance": 1047.63689283956,    
        }

        # print(from_to_nodes[0]["obj_id"])

        for node_index, node in enumerate(from_to_nodes):
            from_node_id = from_to_nodes[node_index]["from_node"]
            to_node_id = from_to_nodes[node_index]["to_node"]

            for road_node in list(csv_road_node)[1:]:

                x_part = road_node[7].split("e")[0]
                y_part = road_node[8].split("e")[0]

                # print(list(road_node)[0])

                if int(list(road_node)[0]) == from_node_id:
                    from_node = { 
                        "x": float(x_part), 
                        "y": float(y_part) 
                    }
1q
                elif int(list(road_node)[0]) == to_node_id:
                    to_node = { 
                        "x": float(x_part), 
                        "y": float(y_part) 
                    }

                    print("from_node")
                    print(from_node)

                    distance_calculations = distance(
                        from_node["x"],
                        to_node["x"],
                        from_node["y"],
                        to_node["y"],
                    )

                    if distance_calculations  < fastest_destination["distance"]:
                        fastest_destination = { 
                            "obj_id": node["obj_id"], 
                            "distance": distance_calculations,     
                        }


        # print(fastest_destination)    
                    
            
