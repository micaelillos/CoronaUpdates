from bs4 import BeautifulSoup
import requests


class city_scraping:
    def __init__(self):
        pass


def get_value(x):
    num = ''
    numbers = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if x[0] in numbers:
        num += x[0]
    i = 1
    while x[i] in numbers:
        num += x[i]
        i += 1
    num = num.split('.')
    return int(num[0]) + int(num[1])*100


def city_places(city):
    stre = "https://www.gov.il/he/departments/news/" + city + "-corona"

    result = requests.get(stre)
    src = result.content
    soup = BeautifulSoup(src, 'html5lib')
    links = soup.find_all("div")
    page = ''
    for link in links:
        page += link.getText()

    for i, letter in enumerate(page):

        if page[i:i+35] == 'מקומות שבהם שהו חולי קורונה מאומתים' or page[i:i+35] == 'מקומות שבהם שהו חולי קורונה מאומתים':
            page = page[i:]

    for i, letter in enumerate(page):
        if page[i:i+13] == 'הנחיות לציבור':
            page = page[:i+13]

    file = open('temp.txt', 'w')
    file.write(page)
    file.close()
    file = open('temp.txt', 'r')
    line = file.readline()
    data = []
    while line != 'הנחיות לציבור':
        if (len(line) > 10 and line[:11] != 'תאריך עדכון') and line != '\n' and line[0] != 'מ':
            if list(line)[0] == '\t':
                data.append(line[1:])
            else:
                data.append(line)
        line = file.readline()

    file.close()
    data.sort(key=lambda x: get_value(x), reverse=True)
    return data
