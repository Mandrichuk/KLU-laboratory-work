import csv 
from math import sin, cos, acos, radians

def distance(lat1, lon1, lat2, lon2):
    """
    Рассчитывает расстояние по великому кругу между двумя точками на поверхности Земли 
    с использованием формулы Хаверсина.

    Параметры:
    - lat1, lon1: Широта и долгота первой точки в градусах.
    - lat2, lon2: Широта и долгота второй точки в градусах.

    Возвращает:
    - Расстояние между двумя точками в километрах.
    """
    inner_part = min(1.0, max(-1.0, sin(radians(lat1)) * sin(radians(lat2)) + cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(lon1) - radians(lon2))))
    return 6373.0 * acos(inner_part)

# Открыть и прочитать CSV-файл с информацией о дорожных узлах
with open("RoadNode.csv", "r") as file:
    csv_reader = csv.reader(file)

    france_locations = []
    germany_locations = []

    # Перебор каждой строки в CSV-файле
    for row in csv_reader:
        # Разделение координат, представленных в научной записи
        x_parts = row[7].split("e")
        y_parts = row[8].split("e")

        # Проверка, соответствует ли строка Франции или Германии, и являются ли координаты допустимыми
        if (row[9] == "France" or row[9] == "Germany") and (len(x_parts) > 1 and len(y_parts) > 1 and x_parts[0] != 'X' and y_parts[0] != 'X'):
            x = float(x_parts[0])
            y = float(y_parts[0])

            # Сохранение информации о местоположении в соответствующих списках
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

    # Расчет расстояния между первыми местоположениями во Франции и Германии
    first_route = distance(
        france_locations[0]["coords"]["x"], 
        france_locations[0]["coords"]["y"], 
        germany_locations[0]["coords"]["x"], 
        germany_locations[0]["coords"]["y"]
    )

    # Инициализация наиболее оптимального маршрута расстоянием и соответствующими идентификаторами узлов
    most_optimal_route = {
        "distance": first_route, 
        "france_id": france_locations[0]["id"], 
        "germany_id": germany_locations[0]["id"]
    } 

    # Перебор всех комбинаций местоположений Франции и Германии для поиска наилучшего маршрута
    for fl_index, fl in enumerate(france_locations):
        for gl_index, gl in enumerate(germany_locations):
            current_route = distance(
                france_locations[fl_index]["coords"]["x"], 
                france_locations[fl_index]["coords"]["y"], 
                germany_locations[gl_index]["coords"]["x"], 
                germany_locations[gl_index]["coords"]["y"]
            )

            # Вывод сравнения текущего маршрута и наилучшего маршрута
            print(f"MOR {most_optimal_route['distance']} & CR {current_route}")

            # Обновление наилучшего маршрута, если текущий маршрут короче
            if current_route < most_optimal_route["distance"]:
                most_optimal_route = {
                    "distance": current_route, 
                    "france_id": france_locations[fl_index]["id"], 
                    "germany_id": germany_locations[gl_index]["id"]
                }

    # Вывод информации о наилучшем маршруте
    print("Наилучший маршрут:")
    print(f"Расстояние: {most_optimal_route['distance']}\nИдентификатор Франции: {most_optimal_route['france_id']}\nИдентификатор Германии: {most_optimal_route['germany_id']}")
