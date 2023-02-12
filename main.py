from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import urllib
import ssl
import sys
if sys.version > '3':
   import urllib.request as urllib2
else:
   import urllib2

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  host = 'https://aliv13.data.moji.com'
  path = '/whapi/json/alicityweather/condition'
  method = 'POST'
  appcode = '816ccb8790ab44739aa230bb37db131c'
  querys = ''
  bodys = {}
  url = host + path

  bodys['cityId'] = '''1286'''
  bodys['token'] = '''50b53ff8dd7d9fa320d3d3ca32cf8ed1'''
  post_data = urllib.urlencode(bodys)
  request = urllib2.Request(url, post_data)
  request.add_header('Authorization', 'APPCODE ' + appcode)
  #根据API的要求，定义相对应的Content-Type
  request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  response = urllib2.urlopen(request, context=ctx)
  content = response.read().json()
  weather = res['data']['condition']
  #url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  #res = requests.get(url).json()
  #weather = res['data']['list'][0]
  return weather['condition'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
