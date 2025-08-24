import http.client
import ssl
import gzip
import zlib
import json
from io import BytesIO


with open('./api_key', 'r', encoding='utf-8') as file:
    APIKEY = file.read()

API = 'airapi.airly.eu'
API_URL = f'https://airapi.airly.eu/v2/measurements/location?locationId=9910&apikey={APIKEY}&Accept-Encoding=gzip'

HEADERS = {'AuhtKeys': 'auth_values'}
# Add the gzip header
HEADERS['Accept-Encoding'] = 'gzip'
HEADERS['Accept'] = 'application/json'

connection = http.client.HTTPSConnection(API, context = ssl._create_unverified_context())
connection.request('GET', API_URL, headers = HEADERS)
response = connection.getresponse()

gzip_file = gzip.GzipFile(fileobj=response)

response = ''

while chunk := gzip_file.read(1024):
    # print(chunk)
    response += chunk.decode('utf-8')
    # response += bytearray(chunk)

data = json.loads(response)
print(data)

if __name__ == '__main__':
    pass