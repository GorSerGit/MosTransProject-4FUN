
# type_area - тип площади
# square_complex - площадь комплекса
# NumPeople - Количество жильцов
# NumWorkPeople - Количество трудоспособного населения
# MassTransport - нагрузка на общественный транспорт
# PersonalCars - Нагрузка на автомобили
# square_live - Жилая площадь
# Not_square_live - Не жилая площадь
# s_25 - Процент площади под 25м2 на человека
# s_45 - Процент площади под 45м2 на человека

def living_area_under_load(s_25, s_45, square_live, Not_square_live):

    S_type = {
        'office': 35,
        'live1':25,
        'live2':45
        }

    People_square_live = int((square_live * s_25 / 100 / S_type['live1']) + (square_live * s_45 / 100 / S_type['live2']))
    People_Not_square_live = int(Not_square_live / S_type['office'])
    
    NumPeople = People_square_live + People_Not_square_live
    NumWorkPeople = int(NumPeople * 0.57)

    MassTransport = int(NumWorkPeople * 0.7)
    PersonalCars = int(NumWorkPeople * 0.3 / 1.2)

    return [MassTransport, PersonalCars]

print(living_area_under_load(25, 75, 100000, 90000))
