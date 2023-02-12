import requests
import os
from dotenv import load_dotenv
load_dotenv()
import json

demo_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
live_url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"

params = {
    "consumer_key" : os.getenv("PESAPAL_CONSUMER_KEY"),
    "consumer_secret" : os.getenv("PESAPAL_CONSUMER_SECRET"),
}
headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}
# send a post request to demourl with params
data = requests.request("POST",demo_url, params=params,headers = headers)

print(data.text)