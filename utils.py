#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__  =   "Jifu Zhao"
__email__   =   "jzhao59@illinois.edu"
__date__    =   "02/20/2018"
__update__  =   "02/20/2018"
"""

import pandas as pd
import requests
import datetime
import calendar
import time

# key for wunderground.com API
KEY = 'ac6a917d396d3bd0'


def query_weather(start_year, end_year, key, state='IL', area='Chicago'):
    """ Qeury the weather information from https://www.wunderground.com
        at the given area in the given time range
    """
    # define url template to query weather
    prefix = 'https://api.wunderground.com/api/'
    url = prefix + '{key}/history_{year}{month}{day}/q/{state}/{area}.json'

    # lists to store the data
    timeList = []
    date = []
    temperature = []
    dewpoint = []
    humidity = []
    precipitation = []
    pressure = []
    rain = []
