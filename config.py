import requests

bot_token = '5876207271:AAHFctyta4siexGi8SaMw73gNWqK5l2zZ4s'
MAIN_URL = f'https://api.telegram.org/bot{bot_token}'

r = requests.get(f'{MAIN_URL}/getMe').json()
# print(r)

bot_name = r['result']['first_name']
chat_id = r['result']['id']
