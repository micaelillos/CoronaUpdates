from bs4 import BeautifulSoup
import requests

def coronatime(name):
    result = requests.get("https://www.worldometers.info/coronavirus/#countries")
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all("td")
    arr = []
    if not name:
        name = "Israel"
    name = name.upper()
    for link in links:
        arr.append(link.getText())
    count = 0
    val = 0
    for a in arr:
        if name in a.upper():
            val = count
            break
        count += 1

    result = []
    for x in range(0, 8):
        result.append(arr[val + x])
    return result

def glo():
    result = requests.get("https://www.worldometers.info/coronavirus/#countries")
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all("span")
    arr = []
    for link in links:
        w = link.getText().replace(" ", "")
        arr.append(w)
    return arr[4:7]


def getop():
    result = requests.get("https://www.worldometers.info/coronavirus/")
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all("td")
    arr=[]
    for link in links:
        w = link.getText().replace(" ", "")
        arr.append(w)
    arr = arr[0:35]
    return arr

