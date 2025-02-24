from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday_1 = os.environ['BIRTHDAY_1']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://api.seniverse.com/v3/weather/now.json?key=S6qE0xJR1cW69c-gy&location=changchun&language=zh-Hans&unit=c"
  res = requests.get(url).json()
  resultwea = res['results'][0]
  now = resultwea['now']
  weather = now['text']
  temperature = math.floor(float(now['temperature']))
  return weather, temperature

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday_1():
  next = datetime.strptime(str(date.today().year) + "-" + birthday_1, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#def get_words():
#  url2 = "https://apis.tianapi.com/caihongpi/index?key=ac823a02d471776347fcf7a71bd91794"
#  wordsres = requests.get(url2).json()
#  words = wordsres['result']['content']
#  return words

def get_words():
    try:
        url = "https://apis.tianapi.com/caihongpi/index?key=ac823a02d471776347fcf7a71bd91794"
        response = requests.get(url)
        response.raise_for_status()  # 如果状态码非200，抛出异常
        wordsres = response.json()
        if wordsres.get('code') == 200:  # 天行数据成功响应
            return wordsres['result']['content']
        else:
            print(f"API Error: {wordsres.get('msg')}")
            return "今天接口有点问题，但你的笑容是最美的彩虹~"
    except Exception as e:
        print(f"Error fetching words: {e}")
        return "遇见你已是今日最幸运的事~"

#def get_words():
#  words = requests.get("https://api.shadiao.pro/chp")
#  if words.status_code != 200:
#    return get_words()
#  return words.json()['data']['text']

#def get_random_color():
#  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
#wordresult = get_words()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"birthday_left_1":{"value":get_birthday_1()},"words":{"value":get_words()}}
res = wm.send_template(user_id, template_id, data)
print(res)
