import os
import time as t
from flask import Flask, render_template, request, flash
import scraping_details
from city_info import get_places
from send_mails import send_all_mails
from lists import *
from city_scraping import city_places

global last_country_data
global israel_data
global glo_data
global time_checked
global top_countries
app = Flask(__name__)


def remove_comas(num):
    new_num = ''
    for i in num:
        if i != ',':
            new_num += i
    return int(new_num)


def update_data(ip):
    global last_country_data
    global israel_data
    global glo_data
    global top_countries
    global time_checked
    first_time = False
    try:
        glo_data[ip]
    except (KeyError, NameError):
        first_time = True

    if first_time or t.time() - time_checked[ip] > 600:
        da = scraping_details.coronatime('')
        last_country_data[ip] = da

        israel_data[ip] = last_country_data[ip]
        glo_data[ip] = scraping_details.glo()
        top_countries[ip] = scraping_details.getop()
        time_checked[ip] = t.time()


@app.route('/')
@app.route('/index/')
def index():
    ip = (request.headers.get('X-Forwarded-For', request.remote_addr))
    update_data(ip)
    global israel_data
    global glo_data
    arr = israel_data[ip]
    glo = glo_data[ip]
    # adding death percentage
    t = remove_comas(glo[0])
    d = remove_comas(glo[1])
    glo.append('{0:.2f}'.format(d / t * 100))
    return render_template('index.html', arr=arr, glo=glo)


@app.route('/form/', methods=['GET', 'POST'])
def country(see_more=''):
    ip = (request.headers.get('X-Forwarded-For', request.remote_addr))
    global last_country_data
    update_data(ip)
    if request.method == 'POST':
        try:
            text = request.form['u']
        except:
            c = request.form['load_more_data']
            user_top_countries = top_countries[ip]
            text = user_top_countries[(int(c) - 1) * 11]

        arr = scraping_details.coronatime(text)
        last_country_data[ip] = arr

    else:
        arr = last_country_data[ip]

    return render_template('country.html', arr=arr, top_c=top_countries[ip])


@app.route('/city/', methods=['GET', 'POST'])
def city():  # city in israel
    if request.method == 'POST':
        city_name = request.form['name']

        if city_name not in get_list_of_cities():  # check if city is a valid city
            msg = 'Not a Valid City'
            return render_template('city.html', msg=msg, city_list=get_list_of_cities())

        city_name = city_name.lower()
        city_name = city_name.replace(' ', '-')
        # special cases
        if city_name == 'tel-aviv':
            city_name = city_name.replace('-', '')
        if city_name == 'rishon-lezion':
            city_name = '-' + city_name

        print(city_name)
        places = city_places(city_name)
        msg = 'List of places in ' + city_name + ':'

        if not places:  # check if there are places in city
            msg = 'no places in ' + city_name

        return render_template('city.html', places=places, msg=msg, city_list=get_list_of_cities())

    else:  # in case of GET request
        return render_template('city.html', city_list=get_list_of_cities())


@app.route('/email/', methods=['GET', 'POST'])
def email_alerts():
    if request.method == 'POST':
        address = request.form['address']
        city_name = request.form['city_name']
        if city_name not in get_list_of_cities():
            flash('Not a valid city!')
        else:
            file = open('mail_list.txt', 'a')
            # add city check/ mail check
            file.write(address + '\n' + city_name + '\n')
            flash('Email added!')

    return render_template('emailalerts.html', city_list=get_list_of_cities())


@app.route('/info/')
def info():
    return render_template('info.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/emailadresslist/')
def send_emails():
    send_all_mails(True)
    return 'done'


if __name__ == '__main__':
    global last_country_data
    global israel_data
    global glo_data
    global top_countries
    global time_checked

    last_country_data = {}
    israel_data = {}
    glo_data = {}
    top_countries = {}
    time_checked = {}

    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


