
from libs.maps import get_stations_and_stops

from libs.People_to import living_area_under_load

import math

import json
import random 

def convert_to_json(input_data):
    # Преобразуем входные данные, заменяя множества на строки
    processed_data = []
    for item in input_data:
        processed_item = {
            'name': list(item['name'])[0],  # берем первый элемент множества
            'type': list(item['type'])[0],  # берем первый элемент множества
            'veroyat': list(item['veroyat'])[0],  # берем первый элемент множества
            'latitude': list(item['latitude'])[0],
            'longitude': list(item['longitude'])[0],
            'People_to_trans': list(item['People_to_trans'])[0],
            'People_to_road_full': list(item['People_to_road_full'])[0]
        }
        processed_data.append(processed_item)
    
    # Преобразуем в JSON формат
    json_data = json.dumps(processed_data, ensure_ascii=False, indent=4)
    return json_data

import random
import math

def calculate_passenger_distribution_ant_colony(distances, num_ants=600, iterations=50, alpha=10, beta=10, evaporation_rate= 1):
    
    num_stops = len(distances)
    pheromone_levels = [1.0] * num_stops  # Инициализация феромонов

    for _ in range(iterations):
        for _ in range(num_ants):
            # Выбор маршрута муравьем
            current_stop = random.randint(0, num_stops - 1)
            visited_stops = [current_stop]
            while len(visited_stops) < num_stops:
                # Выбор следующей остановки
                next_stop = choose_next_stop(current_stop, distances, pheromone_levels, visited_stops, alpha, beta)
                current_stop = next_stop
                visited_stops.append(current_stop)

            # Обновление феромонов на маршруте
            update_pheromones(visited_stops, pheromone_levels, distances, evaporation_rate)

    # Расчет вероятностей после завершения итераций
    probabilities = [pheromone_levels[i] / sum(pheromone_levels) for i in range(num_stops)]
    # Перевод в проценты
    probabilities = [round(probability * 100, 2) for probability in probabilities]

    return probabilities

def choose_next_stop(current_stop, distances, pheromone_levels, visited_stops, alpha, beta):

    available_stops = [i for i in range(len(distances)) if i not in visited_stops]
    probabilities = {}

    for stop in available_stops:
        distance = distances[stop]
        pheromone = pheromone_levels[stop]
        probabilities[stop] = (pheromone ** alpha / distance ** beta)**0.5

    # Нормализация вероятностей
    sum_probabilities = sum(probabilities.values())
    normalized_probabilities = {stop: probability / sum_probabilities for stop, probability in probabilities.items()}

    # Выбор следующей остановки
    next_stop = random.choices(list(normalized_probabilities.keys()), weights=list(normalized_probabilities.values()))[0]
    return next_stop

def update_pheromones(visited_stops, pheromone_levels, distances, evaporation_rate):
    
    for i in range(len(visited_stops) - 1):
        current_stop = visited_stops[i]
        next_stop = visited_stops[i+1]
        distance = distances[next_stop]
        pheromone_levels[next_stop] = (1 - evaporation_rate) * pheromone_levels[next_stop] + 1 / distance



def analyse(latitude, longtitude, s_25, s_45, square_live, Not_square_live):
    # Пример координат и радиуса
    latitude = latitude # Широта
    longitude = longtitude  # Долгота
    radius = 600  # Радиус в метрах

    
    # Получаем список ближайших станций транспорта и их параметры
    stations_and_stops = get_stations_and_stops(latitude, longitude, radius)

    dist = []
    name = []
    tip = []
    Mlatitude = []
    Mlongitude= [] 
    
    for place in stations_and_stops:
        dist.append(place['distance'])
        name.append(place['name'])
        tip.append(place['type'])
        Mlatitude.append(place['latitude'])
        Mlongitude.append(place['longitude'])

    # Вывод инфы по вероятностям
    stations = calculate_passenger_distribution_ant_colony(dist)

    m = []

    i = 0

    stek = []
    
    for place1 in stations_and_stops:
        veroyati = 0
        j=0
        if place1['name'] not in stek:
            stek.append(place1['name'])
            for place2 in stations_and_stops:
                if place1['name'] == place2['name'] and place1['type'] == place2['type']:
                    veroyati = veroyati + stations[j]
                j = j + 1

            NPeople = living_area_under_load(s_25, s_45, square_live, Not_square_live)
            
                        
            m.append({"name": {name[i]}, "type": {tip[i]}, "veroyat": {float(str(veroyati)[0:5])}, "latitude": {Mlatitude[i]},
                      "longitude": {Mlongitude[i]}, "People_to_trans":{int(NPeople[0] / 100 * float(str(veroyati)[0:5]))},
                      "People_to_road_full":{int(NPeople[1])}})

        i = i + 1

    


    json_output = convert_to_json(m)

    return m

if __name__ == "__main__":
    print(analyse(55.671366, 37.613603, 25, 75, 100000, 90000))
