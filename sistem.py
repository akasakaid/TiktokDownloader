import os
import json
import re
import time
import requests
import random
import tiktok_module
from requests import *
from datetime import datetime
from config import *

api = f"https://api.telegram.org/bot{token_bot}/"
update_id = 0
last_use = 1

def SendVideo(userid,msgid):
	res = post(f"{api}sendvideo",
    data={"chat_id":userid,
      "caption":"<b>Video Downloaded from</b> @TiktokVideoDownloaderIDBot!\n\n<b>EN</b> : <i>if video blank send url again!</i>\n<b>ID</b> : <i>jika video putih kirim url lagi</i>",
      "parse_mode":"html",
      "reply_to_message_id":msgid,
      "reply_markup":json.dumps(
        {"inline_keyboard":[
          [
            {"text":"Support Me ^-^",
            "url":"https://www.youtube.com/channel/UCTjTQErgDA79Owo6tnYN0PQ?sub_confirmation=1"
            }
          ]
          ]
        }
      )},
    files={"video":open("video.mp4","rb")})

def SendMsg(userid,text,msgid):
	post(f"{api}sendmessage",
    json={
      "chat_id":userid,
      "text":text,
      "parse_mode":"html",
      "reply_to_message_id":msgid
    }
  )

def get_time(tt):
	ttime = datetime.fromtimestamp(tt)
	return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"

def Bot(update):
  try:
    global last_use
    userid = update['message']['chat']['id']
    pesan = update['message']['text']
    msgid = update['message']['message_id']
    timee = update['message']['date']
    if update['message']['chat']['type'] != "private":
      SendMsg(userid,"Bot only work in private chat !",msgid)
      return
    first_name = update['message']['chat']['first_name']
    print(f"{get_time(timee)}-> {userid} - {first_name} -> {pesan}")
    if pesan.startswith('/start'):
      SendMsg(userid,"<b>Welcome to Tiktok Video Downlaoder Bot !</b>\n\n<b>How to use this bot </b>:\n<i>just send or paste url video tiktok on this bot </i>!!\n",msgid)
    elif "tiktok.com" in pesan and "https://" in pesan :
      getvid = tiktok_module.Tiktok().musicallydown(url=pesan)
      if getvid == False:
        SendMsg(userid,"<i>Failed to download video</i>\n\n<i>Try again later</i>",msgid)
        return
      elif getvid == "private/removed":
        SendMsg(userid,"<i>Failed to download video</i>\n\n<i>Video was private or removed</i>",msgid)
      elif getvid == "file size is to large":
        SendMsg(userid,"<i>Failed to download video</i>\n\n<i>Video size to large</i>",msgid)
      else:
        SendVideo(userid,msgid)
    elif "/help" in pesan:
      SendMsg(userid,"How to use this bot :\njust send or paste url tiktok video on this bot !\n\n/donation - for donation bot\n/status - show status bot",msgid)
    elif pesan.startswith("/donation"):
      SendMsg(userid,"Support me on\n\nko-fi (EN): https://ko-fi.com/fowawaztruffle\nsaweria (ID): https://saweria.co/fowawaztruffle\ntrakteerid (ID): https://trakteer.id/fowawaz\nQRIS (EWALLET,BANK): https://s.id/nusantara-qr",msgid)
  except KeyError:
    return
