from time import sleep
from requests import get
from requests.exceptions import *
from system import Bot
from dotenv import dotenv_values

token_bot = dotenv_values()['token_bot']

api = "https://api.telegram.org/bot" + token_bot + "/"
update_id = 0

print("BOT ACTIVED")
print("PRESS CTRL + C TO EXIT ")
while True:
    try:
        req = get(
            f"https://api.telegram.org/bot{token_bot}/getupdates", params={"offset": update_id}).json()
        if len(req['result']) == 0:
            continue
        try:
            update = req["result"][0]
            Bot(update)
            update_id = update['update_id'] + 1
            print("-"*40)
        except KeyError:
            continue
    except KeyboardInterrupt:
        exit()
    except ConnectionError:
        print('- connection error!,try again after 5 seconds !')
        sleep(5)
        continue
