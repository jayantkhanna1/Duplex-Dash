import random
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

price = 1
params = {
    "consumer_key": os.getenv("CONSUMER_KEY"),
    "consumer_secret": os.getenv("CONSUMER_SECRET"),
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
mpesa_url_1 = os.getenv("MPESA_URL_1")
data = requests.post(mpesa_url_1, json=params)
token = data.json()['token']

# IPN
mpesa_url_2 = os.getenv("MPESA_URL_2")
headers = {
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}
params = {
    "url": os.getenv("BASE_URL")+"ipn",
    "ipn_notification_type": "POST",
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
}
data = requests.post(mpesa_url_2, json=params, headers=headers)
ipn_data = data.json()

# Getting IPN endpoints
mpesa_url_3 = os.getenv("MPESA_URL_3")
headers = {
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}
params = {
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
}
data = requests.get(mpesa_url_3, headers=headers, params=params)

# Submitting payment request
mpesa_url_4 = os.getenv("MPESA_URL_4")
headers = {
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}
params = {
    "Authentication": "Bearer " + token,
    "Authorization": "Bearer " + token,
    "id": random.randint(1, 100000000),
    "currency": "USD",
    "amount": str(price),
    "description": "test",
    "callback_url": os.getenv("BASE_URL")+"paymentConfirmation",
    "notification_id": ipn_data['ipn_id'],
    "billing_address": {
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

data = requests.post(mpesa_url_4, json=params, headers=headers)
submit_data = data.json()
print(submit_data["redirect_url"])
