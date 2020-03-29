from bs4 import BeautifulSoup
import requests

'''''
newdict = {1:0, 2:0, 3:0}
print(len([*newdict]))
'''

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
    if len(num) > 1:
        return int(num[0]) + int(num[1])*100
    else:
        num = ''
        numbers = ['/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if x[0] in numbers:
            num += x[0]
        i = 1
        while x[i] in numbers:
            num += x[i]
            i += 1

        num = num.split('/')

        if len(num) > 1:
            return int(num[0]) + int(num[1]) * 100

        else:
            print('problem')
            return 0


if __name__ == '__main__':
    stre = "https://www.gov.il/he/departments/news/" + 'netanya' + "-corona"

    result = requests.get(stre)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
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
    print(page)
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
    print(data)