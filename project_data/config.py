import requests

bot_token = '5994116282:AAHZP-VlffiYk9AijzRYOM69d2tACoWCMaQ'
MAIN_URL = f'https://api.telegram.org/bot{bot_token}'

r = requests.get(f'{MAIN_URL}/getMe').json()
# print(r)

bot_name = r['result']['first_name']
chat_id = r['result']['id']
