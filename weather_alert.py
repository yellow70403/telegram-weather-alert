import os
import requests


LOCATION_NAME = "桃園市"
LATITUDE = 24.9937
LONGITUDE = 121.3010
RAIN_THRESHOLD = 60


def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Taipei",
        "forecast_days": 1
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    date = data["daily"]["time"][0]
    rain = data["daily"]["precipitation_probability_max"][0]

    return date, rain


def send_telegram(message):

    bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    print("正在傳送 Telegram...")
    print("Chat ID 已取得")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": message
        },
        timeout=30
    )

    print("Telegram HTTP 狀態碼：", response.status_code)
    print("Telegram 回應：", response.text)

    response.raise_for_status()


def main():

    date, rain = get_weather()

    print("========== 天氣資料 ==========")
    print(f"日期：{date}")
    print(f"地點：{LOCATION_NAME}")
    print(f"降雨機率：{rain}%")
    print("==============================")


    # 強制測試 Telegram
    message = (
        "☔ Telegram 測試通知\n\n"
        f"日期：{date}\n"
        f"地點：{LOCATION_NAME}\n"
        f"目前降雨機率：{rain}%\n\n"
        "如果你看到這則訊息，代表 Telegram Bot 已經成功連線！"
    )

    send_telegram(message)

    print("Telegram 通知傳送成功！")


if __name__ == "__main__":
    main()
