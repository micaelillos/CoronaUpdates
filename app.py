import os
import time as t
from flask import Flask, render_template, request, flash
import scraping_details
from city_info import get_places
from send_mails import send_all_mails
from lists import *

global last_country_data
global israel_data
global glo_data
global time_checked
global top_countries
app = Flask(__name__)


def update_data():
    global last_country_data
    global israel_data
    global glo_data
    global top_countries
    global time_checked
    first_time = False
    try:
        glo_data
    except NameError:
        first_time = True
    if t.time() - time_checked > 600 or first_time:
        last_country_data = scraping_details.coronatime('israel')
        israel_data = last_country_data
        glo_data = scraping_details.glo()
        top_countries = scraping_details.getop()
        time_checked = t.time()


@app.route('/')
@app.route('/index/')
def index():
    update_data()
    global israel_data
    global glo_data
    arr = israel_data
    glo = glo_data
    return render_template('index.html', arr=arr, glo=glo)


@app.route('/form/', methods=['GET', 'POST'])
def country(see_more=''):
    print(see_more)
    global last_country_data
    update_data()
    if request.method == 'POST':
        text = request.form['u']
        arr = scraping_details.coronatime(text)
        last_country_data = arr
    else:
        arr = last_country_data
    return render_template('country.html', arr=arr, top_c=top_countries)


@app.route('/city/', methods=['GET', 'POST'])
def city():  # city in israel
    if request.method == 'POST':
        city_name = request.form['name']
        print(city_name)
        places = get_places(city_name)
        msg = 'List of places in ' + city_name + ':'
        if not places:
            msg = 'no places in ' + city_name
        if places is None:
            msg = 'not a valid city'
            places = []

        return render_template('city.html', places=places, msg=msg)

    else:
        return render_template('city.html')


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

    return render_template('emailalerts.html')


@app.route('/info/')
def info():
    return render_template('info.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/emailadresslist/')
def send_emails():
    send_all_mails(False)
    return 'done'


if __name__ == '__main__':
    global time_checked
    time_checked = t.time()
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
