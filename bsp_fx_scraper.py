#!/usr/bin/env python3
import requests
import csv
import os
import time
import sys
from bs4 import BeautifulSoup
from datetime import datetime

url = "http://www.bsp.com.pg/International/Exchange-Rates/Exchange-Rates.aspx"
data, country_code, csv_file, csv_codes = {}, {}, "./bsp_rates.csv", "./cc.csv"


def get_fx_rates():
    global url, data

    r = requests.get(url, timeout=15)
    if not r.status_code == 200:
        raise ConnectionError("Check Internet Connection")
    print('Updating csv data-stores...')

    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', attrs={'id': 'exchange_rates'}).find('tbody')
    tbody = table.find_all('tr')

    for i, rate in enumerate(tbody):
        rate = rate.text.strip().split('\n')
        ccode, country, value = rate[4], rate[3], rate[5]
        data[ccode] = float(value)
        country_code[ccode.lower()] = country


def save_csv_rates():
    # Save rates to HD so we dont keep fetching rate from the net
    print(f"Saving fx rates to: {csv_file}")
    with open(csv_file, "w", newline="\n") as f:
        fields = ['country', 'rate']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, country in enumerate(data):
            w.writerow({'country': country.lower(), 'rate': data[country]})


def save_csv_country_codes():
    # Save country codes
    print(f"Saving Country Codes to {csv_codes}")
    with open(csv_codes, "w", newline="\n") as f:
        fields = ['code', 'country']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, code in enumerate(country_code):
            w.writerow({'code': code, 'country': country_code[code]})


def read_csv_rate():
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for i, rate in enumerate(reader):
            data[rate['country']] = float(rate['rate'])


def read_csv_country_codes():
    with open(csv_codes, "r") as f:
        reader = csv.DictReader(f)
        for i, code in enumerate(reader):
            country_code[code['code']] = code['country']


def init():
    if not os.path.isfile(csv_file):
        print(f"Getting fresh rates...")
        get_fx_rates()
        save_csv_rates()
        save_csv_country_codes()

    todays_date = time.time()
    creation_date = os.path.getctime(csv_file)
    dcreation_date = datetime.utcfromtimestamp(
        creation_date).strftime('%Y-%m-%d %H:%M:%S')
    # 86400: the number of seconds in a day
    if todays_date - creation_date > 86400:
        print(f"Rates last updated: {dcreation_date}")
        print("Updating exchange rates.")
        get_fx_rates()
        save_csv_rates()
    read_csv_rate()


def convert(c_code, amt):
    if not valid_c_code(c_code):
        print("\n** Invalid Country Code! **\n")
        print(usage)
        exit(1)
    print(
        f"Converting {amt} ({c_code}) {country_code[c_code].capitalize()} to PNG Kina (PGK)")
    for i, cc in enumerate(data):
        if c_code == cc:
            print(f"Rate for {cc.capitalize()} is {data[cc]}")
            print("The converted ammount is: K{:.2f}".format(
                float(amt) / data[cc]))


def show_codes():
    if not os.path.isfile(csv_codes):
        get_fx_rates()
        save_csv_country_codes()
    read_csv_country_codes()
    print("\nCode:\tCountry:")
    print("================================")
    for i, code in enumerate(country_code):
        print(f"{code}\t{country_code[code]}")


def valid_c_code(code):
    read_csv_country_codes()
    if not country_code:
        get_fx_rates()
        save_csv_country_codes()
        read_csv_country_codes()

    if code in country_code:
        return True
    return False


usage = f'''
USAGE:
======\n
    > python {sys.argv[0]} <country code> <ammount in foreign currency>

    eg:
    > python {sys.argv[0]} usd 1999.19

NOTE:
=====\n
    > To get valid country codes, just type:
    > python {sys.argv[0]} codes
'''

if __name__ == '__main__':
    length = len(sys.argv)
    if length == 2:
        if sys.argv[1] == 'codes':
            show_codes()
            exit(0)
        else:
            print("\n** Need Help **")
            print(usage)
    elif length == 3:
        country = sys.argv[1]
        pgk = sys.argv[2]
        init()
        convert(country, pgk)
        exit(0)
    else:
        print("Not enough info to perform exchange calculation")
        print(usage)
