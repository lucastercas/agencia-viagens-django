#!/usr/bin/env python
from requests_html import HTMLSession
import bs4

def get_flights():
    params = [
        '18', '2018-06',
        '17', '2018-07',
        'SAO', 'RIO',
        '1', 'ida_vuelta',
        'S%25C3%25A3o%2520Lu%25C3%25ADs&', 'RIO',
        'S%25C3%25A3o%2520Paulo&', 'SAO',
        '1',
        '16%2F06%2F2018&', '17%2F07%2F2018&',
        'Y', '1', '0', '0',
    ]
    url = "https://www.latam.com/pt_br/apps/personas/booking?fecha1_dia={0}&fecha1_anomes={1}&fecha2_dia={2}&fecha2_anomes={3}&from_city2={4}&to_city2={5}&auAvailability={6}&ida_vuelta={7}&vuelos_origen={8}&from_city1={9}&vuelos_destino={10}&to_city1={11}&flex={12}&vuelos_fecha_salida_ddmmaaaa={13}&vuelos_fecha_regreso_ddmmaaaa={14}&cabina={15}&nadults={16}&nchildren={17}&ninfants={18}".format(*params)
    r = get_session(url)
    flights = parse_html(r)
    return flights

def get_session(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout=10, sleep=10)
    return r

def parse_html(r):
    prices = r.html.find('.value')
    departures = r.html.find('.departure')
    arrivals = r.html.find('.arrival')
    date = r.html.find('.trip-dates', first=True)
    date = date.find('time')
    dates = []
    for d in date:
        dates.append(d.attrs['datetime'])

    flights = []
    for (price, dep, arr) in zip(prices, departures, arrivals):
        flight = {}
        flight['price'] = price.text
        time = dep.find('time')
        aeroport = dep.find('abbr')
        for t in time:
            flight['dep_time'] = t.attrs['datetime']
        for aero in aeroport:
            flight['dep_sig'] = aero.text
            flight['dep_title'] = aero.attrs['title']
        time = arr.find('time')
        aeroport = arr.find('abbr')
        for t in time:
            flight['arr_time'] = t.attrs['datetime']
        for aero in aeroport:
            flight['arr_sig'] = aero.text
            flight['arr_title'] = aero.attrs['title']
        flights.append(flight)
    return flights

def print_flights(flights, dates):
    print('flights from '+dates[0]+' to '+dates[1])
    for flight in flights:
        print(flight['price'], flight['dep_time'], flight['dep_sig'],
              flight['dep_title'], flight['arr_time'], flight['arr_sig'],
              flight['arr_title'])
