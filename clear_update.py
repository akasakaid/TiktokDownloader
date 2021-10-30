from requests import get
import requests
from sistem import Bot
import json
open_config = json.loads(open("config.json").read())
api = f"https://api.telegram.org/bot{open_config['token_bot']}/"
update_id = 0
while True:
	try:
		req = get(f"https://api.telegram.org/bot{open_config['token_bot']}/getupdates",params={"offset":update_id}).json()
		if len(req['result']) == 0:
			continue
		for update in req['result']:
			try:
				Bot(update)
				update_id = update['update_id'] + 1
				print("-"*40)
			except KeyError:
				continue
	except KeyboardInterrupt:
		exit()
	except requests.exceptions.ConnectionError:
		continue
	except requests.exceptions.SSLError:
		continue
