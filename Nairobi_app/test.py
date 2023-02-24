import requests
import os
from dotenv import load_dotenv
load_dotenv()
import json
import random

'''
Token
'''
demo_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
live_url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"

params = {
    "consumer_key" :  "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW",
    "consumer_secret" : "osGQ364R49cXKeOYSpaOnT++rHs=",
}
headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}
# send a post request to demourl with params
data = requests.post(demo_url, json=params)
token = data.json()['token']


'''
IPN
'''
demo_ipn_url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"
live_ipn_url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"
    
headers={
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}
params = {
    "url" : "https://759f-14-139-239-130.in.ngrok.io/ipn", # Ngrok
    "ipn_notification_type":"POST",
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
}

data = requests.post(demo_ipn_url, json=params, headers=headers)
ipn_data = data.json()


'''
getting registered ipn endpoints
'''
reg_ipn_demo_url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/GetIpnList"
reg_ipn_live_url = "https://pay.pesapal.com/v3/api/URLSetup/GetIpnList"

headers={
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "Accept" : "application/json", 
    "Content-Type" : "application/json"
}
params = {
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
}

data = requests.get(reg_ipn_demo_url, headers=headers, params=params)


'''
submitting order
'''

demo_submit_url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"
live_submit_url = "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest"

headers={
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}
params = {
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "id" : random.randint(1, 100000000),
    "currency" : "USD",
    "amount" : "1",
    "description" : "test",
    "callback_url" : "https://759f-14-139-239-130.in.ngrok.io/paymentConfirmation",
    "notification_id" : ipn_data['ipn_id'],
    "billing_address" :{
        "email_address": "john.doe@example.com",
        "phone_number": "0723xxxxxx",
        "country_code": "KE",
        "first_name": "John",
        "last_name": "Doe",
        "city": "Nairobi",
        "postal_code": "00100",
        "address_line1": "123 Main Street",
        "address_line2": "Apartment 1"
    }
}

data = requests.post(demo_submit_url, json=params, headers=headers)
submit_data = data.json()
# Log order id
#url = submit_data['redirect_url']
print(submit_data)