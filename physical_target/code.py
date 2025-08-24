# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Updated for Circuit Python 9.0

import os

import adafruit_connection_manager
import wifi

import adafruit_requests

import zlib

# Get ApiKey, WiFi details, ensure these are setup in settings.toml
APIKEY = os.getenv("API_KEY")
SSID = os.getenv("CIRCUITPY_WIFI_SSID")
PASSWORD = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
rssi = wifi.radio.ap_info.rssi


# URL for GET request
JSON_GET_URL = f'https://airapi.airly.eu/v2/measurements/location?locationId=9910&apikey={APIKEY}&Accept-Encoding=gzip'
# Define a custom header as a dict.

print(f"\nConnecting to {SSID}...")
print(f"Signal Strength: {rssi}")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(SSID, PASSWORD)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")

# Define a custom header as a dict.
HEADERS = {'AuhtKeys': 'auth_values'}
# Add the gzip header
HEADERS['Accept-Encoding'] = 'gzip'
HEADERS['Accept'] = 'application/json'

# print(f" | Fetching URL {JSON_GET_URL}")

# Use with statement for retreiving GET request data
with requests.get(JSON_GET_URL, headers=HEADERS) as response:
    print(response)

    if response.status_code == 200:
        print(f" | 🆗 Status Code: {response.status_code}")
    else:
        print(f" | ❌ Status Code: {response.status_code}")

    with open("/sd/response.gz", "wb") as f:
        f.write(response.content)

    # Decompressing data
    data = response
    decompressed = zlib.decompress(data, 31)
    print(decompressed.decode("utf-8"))
