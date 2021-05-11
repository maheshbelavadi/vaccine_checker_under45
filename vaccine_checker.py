from datetime import datetime, timedelta
import time
import schedule
import requests
import re
from twilio.rest import Client

account_sid = '<twilio sid here>'
auth_token = '<auth token here>'
account_phone_number = '<twilio number here>'
phone_number_to_call = '<your number here>'

# T0 get the area code:
# 1) Get the state code under https://cdn-api.co-vin.in/api/v2/admin/location/states
# 2) Get the area code from https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state code>
# '265' = Bangalore Urban
# '294' = BBMP
# NOTE: By adding area code you will get a call for anywhere in the city. 
#       Better to use only pincode to restrice the search for limited set 
#       of areas in a large city like Bangalore, Mumbai etc 
areacodes = ['265', '294']
pincodes = ['560078', '570017']

def check_vaccine_availability():
    try:
        for areacode in areacodes:
            query_cowin(areacode, False)
        for pin in pincodes:
            query_cowin(pin, True)
    except:
        print("Something went wrong. But I am still alive.")


def query_cowin(code, is_pincode):
    date_to_check = (datetime.today() + timedelta(days=1)).strftime('%d-%m-%Y')
    query_url = 'api/v2/appointment/sessions/public/calendarByDistrict?district_id'
    if is_pincode:
        query_url = 'api/v2/appointment/sessions/public/calendarByPin?pincode'
    query_url = 'https://www.cowin.gov.in/{}={}&date={}'.format(
        query_url, code, date_to_check)
    print(query_url)
    response = requests.get(query_url)
    vaccine_center_list = response.json()
    check_availability(code, vaccine_center_list)


def check_availability(code, vaccine_center_list):
    for center in vaccine_center_list['centers']:
        if 'sessions' in center:
            for session in center['sessions']:
                if(session['available_capacity'] > 0 and session['min_age_limit'] < 45):
                    print('{} Yeppi vaccine available :) for {}. Search code: {}, {}, {}, {}, {}'.format(
                        datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                        session['date'],
                        code,
                        session['available_capacity'],
                        session['vaccine'],
                        center['name'],
                        center['address']))
                    if(session['available_capacity'] > 10):
                        callme('We have found {} {} vaccine available at {}, {}'.format(
                            session['available_capacity'],
                            session['vaccine'],
                            center['name'],
                            center['address']))


def callme(message):
    if bool(re.match("^[A-Za-z0-9]*$", account_sid)) and \
            bool(re.match("^[A-Za-z0-9]*$", account_sid)):
        client = Client(account_sid, auth_token)
        client.calls.create(
            twiml='''<Response><Say>Hi there!! {}. \
               Get vaccinated, stay healthy  </Say></Response>'''.format(message),
            to=phone_number_to_call,
            from_=account_phone_number
        )
    else:
        print('Cannot call back. Incorrect Twilio configuration. Refer readme')


#check_vaccine_availability()
schedule.every(15).seconds.do(check_vaccine_availability)
print('Vaccine monitoring started.')
while True:
    schedule.run_pending()
    time.sleep(1)
