from bs4 import BeautifulSoup
import requests
from lists import get_list_of_places


class scraping:
    def __init__(self):
        pass


def scrape():
    result = requests.get("https://www.google.com/maps/d/viewer?mid=1OGHTakRrv3op0NszI1nCaVEyunQM7xmu&ll=31.880615415550885%2C35.168179049999935&z=8")
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all("div")
    helper = links[0].getText().split("\n")
    var = helper[6].split(",")
    arr = []
    rep = "[\\n" + '"'
    for v in var:
        if any("\u0590" <= c <= "\u05EA" for c in v):
            s = v.replace("]", "")
            for r in rep:
               s = s.replace(r, "")
            arr.append(s)
            if "תיאור" in v:
                break

    arr.remove(arr[-1])
    arr.remove(arr[2])
    arr.remove(arr[-3])

    file = open('list_of_new_places', 'w')
    places = arr
    for line in places:
        file.writelines(line)
        file.writelines('\n')

    file.close()
