import os
import requests


# 可以自行修改的設定
LOCATION_NAME = "桃園市"
LATITUDE = 24.9937
LONGITUDE = 121.3010
RAIN_THRESHOLD = 60


def get_weather():
    """取得今日最高降雨機率。"""

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Taipei",
        "forecast_days": 1,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    forecast_date = data["daily"]["time"][0]
    rain_probability = data["daily"]["precipitation_probability_max"][0]
    return forecast_date, rain_probability


def send_telegram(message):
    """透過Telegram Bot傳送訊息。"""

    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.post(
        url,
        data={"chat_id": chat_id, "text": message},
        timeout=30,
    )

    if not response.ok:
        print("Telegram API錯誤：", response.status_code)
        print("Telegram回覆：", response.text)

    response.raise_for_status()


def main():
    forecast_date, rain_probability = get_weather()

    print(f"預報日期：{forecast_date}")
    print(f"地點：{LOCATION_NAME}")
    print(f"今日最高降雨機率：{rain_probability}%")

    force_send = os.getenv("FORCE_SEND", "false").lower() == "true"

    if rain_probability > RAIN_THRESHOLD or force_send:
        message = (
            "【今日天氣提醒】\n\n"
            f"日期：{forecast_date}\n"
            f"地點：{LOCATION_NAME}\n"
            f"今日最高降雨機率：{rain_probability}%\n\n"
            "今天記得帶傘！"
        )

        if force_send and rain_probability <= RAIN_THRESHOLD:
            message += "\n\n本訊息為手動測試。"

        send_telegram(message)
    print("Telegram通知傳送成功。")
    else:
    print("降雨機率未超過60%，本次不傳送通知。")


if __name__ == "__main__":
    main()
