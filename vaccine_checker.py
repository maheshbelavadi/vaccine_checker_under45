from datetime import datetime, timedelta
import time
import schedule
import requests
import re
from twilio.rest import Client
import urllib.request
from urllib.request import Request, urlopen
import json
import sys

account_sid = '<twilio sid here>'
auth_token = '<auth token here>'
account_phone_number = '<twilio number here>'
phone_number_to_call = '<your number here>'

choice = input('''Please select to below search option
Enter 0 : To search using area code
Enter 1 : To search using pincodes: \n''')

if choice == '0':
    
    state_code_link = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    state_name = input('Please enter the name of state:\n')
    try:
        with urllib.request.urlopen(Request(state_code_link, headers={'User-Agent': 'Mozilla/5.0'})) as url:
            data = json.loads(url.read())['states']
            for item in data:
                if item['state_name'].lower() == state_name.lower().strip():
                    state_code = item['state_id']
                    break
    except:
        state_code = input('Auto state-code fetch not working, please refer the following link for state-code:\n'+ area_codes_link)

    area_codes_link = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + str(state_code)
    try:
        with urllib.request.urlopen(Request(area_codes_link, headers={'User-Agent': 'Mozilla/5.0'})) as url:    
            data = json.loads(url.read())['districts']
            for district in data:
                temp = list(district.values())
                print(f'{temp[1]:<30} {temp[0]:>5}')
                print(f'-'*40)
    except:
        print('Auto area-code fetch not working, please refer the following link for area-codes:\n'+ area_codes_link)
    input_codes = input('Please enter the area-codes seperated by comma(,): \n')
    input_codes = input_codes.split(',')
    area_codes = [(code.strip()) for code in input_codes]

elif choice == '1':
    input_codes = input('Please enter the pin-codes seperated by comma(,): \n')
    input_codes = input_codes.split(',')
    pin_codes = [(code.strip()) for code in input_codes]

else:
    print('Enter valid choice: 0 or 1.')
    sys.exit()

# T0 get the area code:
# 1) Get the state code under https://cdn-api.co-vin.in/api/v2/admin/location/states
# 2) Get the area code from https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state code>
# '265' = Bangalore Urban
# '294' = BBMP
# NOTE: By adding area code you will get a call for anywhere in the city. 
#       Better to use only pincode to restrice the search for limited set 
#       of areas in a large city like Bangalore, Mumbai etc 

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
