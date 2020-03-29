class lists:
    def __init__(self):
        pass


def get_list_of_cities():
    return ['Afula', 'Akko', 'Arad', 'Ariel', 'Ashdod', 'Ashkelon', 'Bat Yam', 'Beer Sheva', 'Beit Shean', 'Beit Shemesh', 'Betar Illit', 'Bnei Berak', 'Dimona', 'Eilat', 'Elad', 'Givatayim', 'Hadera', 'Haifa', 'Herzliya', 'Hod HaSharon', 'Holon', 'Jerusalem', 'Karmiel', 'Kfar Sava', 'Kiryat Ata', 'Kiryat Bialik', 'Kiryat Gat', 'Kiryat Malachi', 'Kiryat Motzkin', 'Kiryat Ono', 'Kiryat Shemone', 'Kiryat Yam', 'Lod', 'Maale Adumim', 'Maalot Tarshiha', 'Migdal HaEmek', 'Modiin', 'Nahariya', 'Nazareth', 'Nes Ziona', 'Nesher', 'Netanya', 'Netivot', 'Nof Hagalil', 'Ofakim', 'Or Akiva', 'Or Yehuda', 'Petah Tikva', 'Raanana', 'Rahat', 'Ramat Hasharon', 'Ramat-Gan', 'Ramla', 'Rehovot', 'Rishon Lezion', "Rosh Ha'ayin", 'Sderot', 'Tel Aviv', 'Tiberias', 'Tira', 'Tirat Carmel', 'Tsfat (Safed)', 'Yavne', 'Yehud-Monosson', 'Yokneam']


def get_list_of_places(file_name='list_of_places'):
    file = open(file_name)
    r = file.readline()
    s = {r}
    last_r = None
    while r != '':
        # print(r[:-1])
        s.add(r[:-1])
        last_r = r
        r = file.readline()

    s.remove(last_r[:-1])
    s.add(last_r)

    # print(len(s))
    # print(s)

    file.close()
    return list(s)

