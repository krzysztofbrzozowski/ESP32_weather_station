import os
import ssl
import socket
import adafruit_connection_manager
import adafruit_requests
import zlib
import json
from adafruit_datetime import datetime, date, time, timezone, timedelta

with open(r'vrtual_target/api_key', 'r', encoding='utf-8') as file:
    API_KEY = file.read()


HEADERS = {'AuhtKeys': 'auth_values'}
# Add the gzip header
HEADERS['Accept-Encoding'] = 'gzip'
HEADERS['Accept'] = 'application/json'

# URL for GET request
JSON_GET_URL = f'https://airapi.airly.eu/v2/measurements/location?locationId=9910&apikey={API_KEY}&Accept-Encoding=gzip'
requests = adafruit_requests.Session(socket, ssl.create_default_context())

def get_data():
    with requests.get(JSON_GET_URL, headers=HEADERS) as r:
        assert r.status_code == 200, \
            f'Expected 200 but got {r.status_code}'

        return r.content

def deflate_data(compressed_content):
    decompressed = zlib.decompress(compressed_content, 31)
    decompressed = decompressed.decode("utf-8")

    try:
        data = json.loads(decompressed)
        iso_date_string = data['current']['tillDateTime']
        # Adding time offset since hour from sensor is delayed by 2hrs
        current_time_isodate = datetime.fromisoformat(iso_date_string) + timedelta(hours=2)
        current_values = data['current']['values']

        text_to_display = ""

        t = current_time_isodate
        text_to_display += f"{t.hour}:{t.minute} {t.day}.{t.month}.{t.year}\n"

        for item in current_values:
            text_to_display += f"{item['name']}: {item['value']}\n"

        print(text_to_display)

    except Exception as e:
        print(e)



if __name__ == '__main__':
    content = get_data()
    deflate_data(content)