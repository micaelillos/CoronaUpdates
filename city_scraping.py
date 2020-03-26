from bs4 import BeautifulSoup
import requests

city = "netanya"
str = "https://www.gov.il/he/departments/news/" + city + "-corona"
print(str)

result = requests.get(str)
src = result.content
print(str+city)
soup = BeautifulSoup(src, 'html5lib')
links = soup.find_all("div")
for link in links:
    print(link.getText())