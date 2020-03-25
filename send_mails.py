from scraping import scrape
from lists import get_list_of_cities, get_list_of_places
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib


class send_mails:
    def __init__(self):
        pass


def send_all_mails(update_list=False):
    scrape()

    old_list = set(get_list_of_places())
    new_list = get_list_of_places('list_of_new_places')
    list_of_cities = get_list_of_cities()
    list_of_places_per_city = {list_of_cities[index]: [] for index in range(len(list_of_cities))}

    new_places = []

    length = len(old_list)
    for place in new_list:
        old_list.add(place)
        if place[0] == ' ':
            place = place[1:]
        if length != len(old_list) and place not in list_of_cities:
            length = len(old_list)
            for i in range(len(place) - 5):
                if place[i:i + 5] == 'u0027':
                    place = place[:i] + place[i + 5:]

            new_places.append(place)

    print(new_places)

    for place in new_places:
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
    ''''
    for city in list_of_cities:
        if list_of_places_per_city[city]:
            print(list_of_places_per_city[city])
    '''
    file = open('mail_list.txt', 'r')
    address = file.readline()
    city_name = file.readline()
    while address != '':
        address = address[:-1]
        city_name = city_name[:-1]
        if list_of_places_per_city[city_name]:
            body = f'List of new places in {city_name}: \n'
            places = list_of_places_per_city[city_name]
            for place in places:
                body += place + '\n'

        else:
            body = f'no new places in {city_name}'

        send_mail(str(body), address)
        address = file.readline()
        city_name = file.readline()

    file.close()

    if update_list is True:
        os.remove('list_of_places')
        file = open('list_of_places', 'w')
        places = get_list_of_places('list_of_new_places')
        for line in places:
            file.writelines(line)
            file.writelines('\n')

        file.close()


def send_mail(body, address):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('corona.in.city.notification@gmail.com', 'timpwmae')
    subject = "עדכוני קורונה"
    message = body

    msg = MIMEMultipart()
    msg['From'] = 'corona.in.city.notification@gmail.com'
    msg['To'] = address
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()
    server.sendmail('corona.in.city.notification@gmail.com', address, text)

    print('Email sent')
    server.quit()



