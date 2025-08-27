import os
import ssl
import socket
import adafruit_connection_manager
import adafruit_requests
import zlib
import json

with open(r'vrtual_target/api_key', 'r', encoding='utf-8') as file:
    API_KEY = file.read()


HEADERS = {'AuhtKeys': 'auth_values'}
# Add the gzip header
HEADERS['Accept-Encoding'] = 'gzip'
HEADERS['Accept'] = 'application/json'

# URL for GET request
JSON_GET_URL = f'https://airapi.airly.eu/v2/measurements/location?locationId=9910&apikey={API_KEY}&Accept-Encoding=gzip'

def get_data():
    requests = adafruit_requests.Session(socket, ssl.create_default_context())
    with requests.get(JSON_GET_URL, headers=HEADERS) as r:
        assert r.status_code == 200, \
            f'Expected 200 but got {r.status_code}'

        return r.content

def deflate_data(compressed_content):
    decompressed = zlib.decompress(compressed_content, 31)
    decompressed = decompressed.decode("utf-8")

    try:
        data = json.loads(decompressed)
    except Exception as e:
        print(e)

    current_values = data['current']['values']
    for item in current_values:
        print(item['name'], item['value'])



if __name__ == '__main__':
    content = get_data()
    deflate_data(content)