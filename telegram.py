from load import *
from pyrogram import Client
from pyrogram import errors

def delete_message(id,messageId):
	bot = Client(name="bot",api_id=ApiId,api_hash=ApiHash,bot_token=TokenBot)
	bot.start()
	try:
		bot.delete_messages(chat_id=id,message_ids=messageId)
		print("[+] message has been delete !")
		bot.stop()
		

	except errors.UserIsBlocked:
		print("[x] user blocked you !")
		bot.stop()

	except errors.PeerIdInvalid:
		print("[x] user maybe died !")
		bot.stop()

def send_message(id,message,replyMessage=False):
	bot = Client(name="bot",api_id=ApiId,api_hash=ApiHash,bot_token=TokenBot)
	bot.start()
	try:
		if replyMessage:
			res = bot.send_message(chat_id=id,text=message,disable_web_page_preview=True,reply_to_message_id=replyMessage)
			print("[+] message has been sending !")
			bot.stop()
			return res

		res = bot.send_message(chat_id=id,text=message,disable_web_page_preview=True)
		print("[+] message has been sending !")
		bot.stop()
		return res

	except errors.UserIsBlocked:
		print("[x] user blocked you !")
		bot.stop()

	except errors.PeerIdInvalid:
		print("[x] user maybe died !")
		bot.stop()

	except Exception as e:
		print(e)
		bot.stop()

def send_video(id,video,caption):
	bot = Client(name="bot",api_id=ApiId,api_hash=ApiHash,bot_token=TokenBot)
	bot.start()
	try:
		res = bot.send_video(chat_id=id,video=open(video,"rb"),caption=caption)
		print('[+] video has been sending !')
		bot.stop()
		if res.video is not None:
			fileId = res.video.file_id
			fileUniqueId = res.video.file_unique_id
		else:
			fileId = res.animation.file_id
			fileUniqueId = res.animation.file_unique_id

		return fileId,fileUniqueId

	except errors.UserIsBlocked:
		print("[x] user blocked you !")
		bot.stop()
		return None,None

	except errors.UserBlocked:
		print("[x] user blocked !")
		bot.stop()
		return None,None

	except errors.PeerIdInvalid:
		print("[x] user maybe died !")
		bot.stop()
		return None,None

