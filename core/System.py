import json
from requests import *
from lib import downloader
from datetime import datetime
from dotenv import dotenv_values
from module.messageText import *
from lib.sendVideo import sendVideo
from lib.sendMessage import sendMessage

token_bot = dotenv_values()['TOKEN_BOT']


def get_time(tt):
    ttime = datetime.fromtimestamp(tt)
    return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"


def Bot(update):
    try:
        if 'callback_query' in str(update):
            userid = update['callback_query']['from']['id']
            first_name = update['callback_query']['from']['first_name']
            meseg = update['callback_query']['data']
            msgid = update['callback_query']['message']['message_id']
            timee = update['callback_query']['message']['date']
            tipeChat = update['callback_query']['message']['chat']['type']
        else:
            userid = update['message']['chat']['id']
            meseg = update['message']['text']
            msgid = update['message']['message_id']
            timee = update['message']['date']
            first_name = update['message']['chat']['first_name']
            tipeChat = update['message']['chat']['type']
        dl = downloader.tiktok_downloader()
        if tipeChat != "private":
            sendMessage(userid, privateText, msgid)
            return
        print(f"{get_time(timee)}-> {userid} - {first_name} -> {meseg}")
        if meseg.startswith('/start'):
            sendMessage(chat_id=userid, message=startText, message_id=msgid)
        elif "tiktok.com" in meseg and "https://" in meseg:
            getvid = dl.musicaldown(url=meseg, output_name="video.mp4")
            if getvid:
                sendVideo(chat_id=userid, video="video.mp4",
                          caption=videoText, message_id=msgid)
                return
            else:
                sendMessage(userid, failedText, msgid)
                return
            # os.remove('video.mp4')
        elif "/help" in meseg:
            sendMessage(
                userid, helpText, msgid)
        elif meseg.startswith("/donation"):
            sendMessage(userid, donationText, msgid)
            return
    except KeyError as e:
        print(f"- {e}")
        open(".log", "a+", encoding="utf-8").write(str(update) + "\n")
        return
