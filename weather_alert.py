import os
import requests

# 地點設定（桃園市）
LOCATION_NAME = "桃園市"
LATITUDE = 24.9937
LONGITUDE = 121.3010

# 降雨機率門檻
RAIN_THRESHOLD = 60


def get_weather():
    """取得今日最高降雨機率"""

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Taipei",
        "forecast_days": 1
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    forecast_date = data["daily"]["time"][0]
    rain_probability = data["daily"]["precipitation_probability_max"][0]

    return forecast_date, rain_probability


def send_telegram(message):
    """傳送 Telegram 通知"""

    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message
        },
        timeout=30
    )

    response.raise_for_status()


def main():

    forecast_date, rain_probability = get_weather()

    print(f"日期：{forecast_date}")
    print(f"地點：{LOCATION_NAME}")
    print(f"最高降雨機率：{rain_probability}%")

    if rain_probability >= RAIN_THRESHOLD:

        message = (
            "☔ 今日下雨提醒\n\n"
            f"日期：{forecast_date}\n"
            f"地點：{LOCATION_NAME}\n"
            f"最高降雨機率：{rain_probability}%\n\n"
            "記得帶傘喔！"
        )

        send_telegram(message)

        print("Telegram通知傳送成功。")

    else:
        print("降雨機率未超過20%，不傳送通知。")


if __name__ == "__main__":
    main()
