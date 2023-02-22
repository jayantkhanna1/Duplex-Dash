import requests
import os
from dotenv import load_dotenv
load_dotenv()
import json

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
data = requests.post(demo_url, json={
    "consumer_key" :  "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW",
    "consumer_secret" : "osGQ364R49cXKeOYSpaOnT++rHs=",
})

print(data.text)