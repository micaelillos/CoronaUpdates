from lists import get_list_of_cities, get_list_of_places


class city_info:
    def __init__(self):
        pass


def get_places(city_name):
    list_of_cities = get_list_of_cities()
    list_of_places = get_list_of_places()
    list_of_places_per_city = {list_of_cities[index]: [] for index in range(len(list_of_cities))}

    if city_name not in list_of_cities:
        return None
    for place in list_of_places:
        words = []
        word = ''
        i = 0
        # print(place)
        for i in range(len(place)):
            if place[i] == ' ':
                words.append(word)
                word = ''
            else:
                word += place[i]
        words.append(word)
        if words[-1] in list_of_cities:
            city = words[-1]
            list_of_places_per_city[city].append(place)
        elif len(words) > 1 and words[-2] + ' ' + words[-1] in list_of_cities:
            city = words[-2] + ' ' + words[-1]
            list_of_places_per_city[city].append(place)

        # print(words)


    return list_of_places_per_city[city_name]
