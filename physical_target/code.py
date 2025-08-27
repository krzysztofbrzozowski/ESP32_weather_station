# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Updated for Circuit Python 10.0 b2

import os
import wifi
import zlib
import json
import time

import adafruit_requests
import adafruit_connection_manager
from adafruit_datetime import datetime, timedelta
from adafruit_magtag.magtag import MagTag

magtag = MagTag()

#Format text_to_display 
magtag.add_text(
    text_scale=1,
    # text_wrap=25,
    text_maxlen=300,
    text_position=(10, 10),
    text_anchor_point=(0, 0),
)

# Get ApiKey, WiFi details, ensure these are setup in settings.toml
APIKEY = os.getenv("API_KEY")
SSID = os.getenv("CIRCUITPY_WIFI_SSID")
PASSWORD = os.getenv("CIRCUITPY_WIFI_PASSWORD")

TIME_BETWEEN_REFRESHES = 1 * 60 * 60  # once a day delay
# TIME_BETWEEN_REFRESHES = 15

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
rssi = wifi.radio.ap_info.rssi

# URL for GET request
JSON_GET_URL = f'https://airapi.airly.eu/v2/measurements/location?locationId=9910&apikey={APIKEY}&Accept-Encoding=gzip'
# Define a custom header as a dict.

# print(f"\nConnecting to {SSID}...")
print(f"Signal Strength: {rssi}")

try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(SSID, PASSWORD)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")

# Define a custom header as a dict
HEADERS = {'AuhtKeys': 'auth_values'}
HEADERS['Accept-Encoding'] = 'gzip'
HEADERS['Accept'] = 'application/json'

# print(f" | Fetching URL {JSON_GET_URL}")

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
        text_to_display += f"{t.hour}:{t.minute}:{t.second} {t.day}.{t.month}.{t.year}\n"

        for item in current_values:
            text_to_display += f"{item['name']}: {item['value']}\n"

        print(text_to_display)

        magtag.set_text(text_to_display)
        magtag.refresh()

    except Exception as e:
        print(e)

# Code execution
content = get_data()
deflate_data(content)
magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES)