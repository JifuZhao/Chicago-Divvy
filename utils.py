#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__  =   "Jifu Zhao"
__email__   =   "jzhao59@illinois.edu"
__date__    =   "02/20/2018"
__update__  =   "02/24/2018"
"""

import pandas as pd
import requests
import calendar
import time


def query_weather(key, year, state='IL', area='Chicago'):
    """ Qeury the weather information from https://www.wunderground.com
        at the given area in the given year (query frequency is limited)
    """
    # define url template to query weather
    prefix = 'https://api.wunderground.com/api/'
    url = prefix + '{key}/history_{year}{month}{day}/q/{state}/{area}.json'

    # lists to store the data
    date_list = []
    temperature = []
    wind_chill = []
    dewpoint = []
    humidity = []
    pressure = []
    visibility = []
    wind_speed = []
    precipitation = []
    events = []
    rain = []
    conditions = []
    errors = []

    # query data for each month
    for month in range(1, 13):
        # get the number of days at the given month
        num_days = calendar.monthrange(year, month)[1]

        # transform into string
        year_str = str(year)
        month_str = str(month)
        if month < 10:
            month_str = '0' + str(month)

        # query the weather for each day
        for day in range(1, num_days + 1):
            day_str = str(day)
            if day < 10:
                day_str = '0' + day_str

            try:
                # query the weather information
                link = url.format(key=key, year=year_str, month=month_str,
                                  day=day_str, state=state, area=area)
                weather = requests.get(link).json()['history']['observations']

                # add new data to list
                for i in range(len(weather)):
                    try:
                        date = weather[i]['date']['year'] + '-' \
                            + weather[i]['date']['mon'] + '-' \
                            + weather[i]['date']['mday'] + '-' \
                            + weather[i]['date']['hour'] + ':' \
                            + weather[i]['date']['min'] + ':00'
                        date_list.append(date)
                        temperature.append(weather[i]['tempi'])
                        wind_chill.append(weather[i]['windchilli'])
                        dewpoint.append(weather[i]['dewpti'])
                        humidity.append(weather[i]['hum'])
                        pressure.append(weather[i]['pressurei'])
                        visibility.append(weather[i]['visi'])
                        wind_speed.append(weather[i]['wspdi'])
                        precipitation.append(weather[i]['precipi'])
                        events.append(weather[i]['icon'])
                        rain.append(weather[i]['rain'])
                        conditions.append(weather[i]['conds'])
                    except:
                        errors.append((month, day, i))
                        continue
                time.sleep(6)
            except:
                errors.append((month, day))

    # transform to DataFrame
    Dict = {'date': date_list, 'temperature': temperature,
            'windchill': wind_chill, 'dewpoint': dewpoint,
            'humidity': humidity, 'pressure': pressure,
            'visibility': visibility, 'wind_speed': wind_speed,
            'precipitation': precipitation, 'events': events,
            'rain': rain, 'conditions': conditions}

    columns = ['date', 'temperature', 'windchill', 'dewpoint', 'humidity',
               'pressure', 'visibility', 'wind_speed', 'precipitation',
               'events', 'rain', 'conditions']
    df = pd.DataFrame(data=Dict, columns=columns)

    return df, errors
