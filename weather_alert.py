import os
import requests


# 可以自行修改的設定
LOCATION_NAME = "桃園市"
LATITUDE = 24.9937
LONGITUDE = 121.3010
RAIN_THRESHOLD = 60


def get_weather():
