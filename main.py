#!/usr/bin/env python3

import time
import urllib
import requests
from bs4 import BeautifulSoup
import threading

last_cases_value = 4326
last_mortos_value = 164

class_conf = 'views-row views-row-3 views-row-odd card mb-3 col-sm-6 col-lg-3'
class_mortes = 'views-row views-row-4 views-row-even views-row-last card mb-3 col-sm-6 col-lg-3'

def Cases_lastDay(value):
    data3 = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=UO1KL3S5VC187M3D&field3={}".format(value))
    data3.close()
    return()

def Mortes_LastDay(value):
    data4 = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=UO1KL3S5VC187M3D&field4={}".format(value))
    data4.close()
    return()

def thread_mortos():
    global last_mortos_value

    while(True):
        page0 = requests.get('https://covid-19.campinas.sp.gov.br/')
        soup0 = BeautifulSoup(page0.text, 'html.parser')

        mortos = soup0.find(class_= class_mortes)
        casos_m = mortos.find_all('span')
        casos_mortos = casos_m[1].contents[0]

        if casos_mortos != last_mortos_value:
            last_update  = requests.get("https://api.thingspeak.com/channels/1083584/fields/2.json?api_key=IK6DZZSK9EBM3H90&results=2").json()
            last_up_date = last_update['channel']['updated_at']
            last_up_mortes_date = last_up_date
            while(last_up_mortes_date == last_up_date):
                Mortes_LastDay(int(casos_mortos)-int(last_mortos_value))
                data1 = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=UO1KL3S5VC187M3D&field2={}".format(casos_mortos))
                data1.close()
                last_up_mortes = requests.get("https://api.thingspeak.com/channels/1083584/fields/2.json?api_key=IK6DZZSK9EBM3H90&results=2").json()
                last_up_mortes_date = last_up_mortes['channel']['updated_at']
                time.sleep(5)
            last_mortos_value = casos_mortos
        time.sleep(3600)

def thread_casos():
    global last_cases_value
    while(True):
        page1 = requests.get('https://covid-19.campinas.sp.gov.br/')
        soup1 = BeautifulSoup(page1.text, 'html.parser')

        confirmados = soup1.find(class_= class_conf)
        casos_c = confirmados.find_all('span')
        casos_confirmados = casos_c[1].contents[0]

        if casos_confirmados != last_cases_value:
            last_update  = requests.get("https://api.thingspeak.com/channels/1083584/fields/1.json?api_key=IK6DZZSK9EBM3H90&results=2").json()
            last_up_date = last_update['channel']['updated_at']
            last_up_cases_date = last_up_date
            while(last_up_cases_date == last_up_date):
                Cases_lastDay(int(casos_confirmados)-int(last_cases_value))
                data0 = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=UO1KL3S5VC187M3D&field1={}".format(casos_confirmados))
                data0.close()
                last_up_cases = requests.get("https://api.thingspeak.com/channels/1083584/fields/1.json?api_key=IK6DZZSK9EBM3H90&results=2").json()
                last_up_cases_date = last_up_cases['channel']['updated_at']
                time.sleep(5)

            last_cases_value = casos_confirmados
        time.sleep(3600)

t1 = threading.Thread(target = thread_mortos, args = [])
t2 = threading.Thread(target = thread_casos, args = [])
print('Start!')
t1.start()
t2.start()
