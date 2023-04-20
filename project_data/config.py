import requests

bot_token = '6086469104:AAG3or7suvI8TaPf1ISZwfmGlBIxrEovRLQ'
MAIN_URL = f'https://api.telegram.org/bot{bot_token}'

r = requests.get(f'{MAIN_URL}/getMe').json()
# print(r)

bot_name = r['result']['first_name']
chat_id = r['result']['id']
