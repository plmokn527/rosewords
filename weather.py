import requests
import time
from datetime import datetime, timedelta

def get_weather(api_key):
    url = f"https://api.seniverse.com/v3/weather/daily.json?key={api_key}&location=chongqing&language=zh-Hans&unit=c&start=0&days=2"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            today_weather = data['results'][0]['daily'][0]
            tomorrow_weather = data['results'][0]['daily'][1]

            current_weather = today_weather['text_day']
            current_temp = today_weather['low'] + '-' + today_weather['high']

            one_day_weather = tomorrow_weather['text_day']

            weather_text = f"""重庆当前天气：{current_weather}，气温：{current_temp}°C
1天后天气：{one_day_weather}"""

            print(weather_text)

        else:
            print("获取天气信息失败，请检查您的网络连接")

    except Exception as e:
        print("获取天气信息失败，请检查您的网络连接")
        print(e)

def main():
    api_key = 'SUFdG3XStZix3a6Bd'  # 请替换为您自己的 API 密钥

    while True:
        get_weather(api_key)
        time.sleep(3600)  # 等待1小时（3600秒）后再次更新天气信息

if __name__ == '__main__':
    main()
