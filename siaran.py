from requests import post
import json

open_config = json.loads(open("config.json").read())
api = f"https://api.telegram.org/bot{open_config['token_bot']}/"

def SendMsg(userid,text):
	post(f"{api}sendmessage",json={"chat_id":userid,"text":text,"parse_mode":"html"})

uus = open("list-userid").read().splitlines()
tot = 1
for user in uus:
	SendMsg(user,"""
Happy 10.000 users 🥳🥳

I apologize if the bot is not responsive, because the server is slow 😔😔
I've run the bot on a server with high specifications

Don't forget to subscribe my youtube channel 😉😉
if you want to donate please type /donation or contact the author 😌👌🏻
		""")
	print(f"siaran : {tot}/{len(uus)} ",flush=True,end='\r')
	tot += 1