'''
so this in my personal function to send message to everyone that use my tiktok downloader bot

tq

regards, AkasakaID
'''

import requests
from lib.sendMessage import sendMessage

textMessage = '''
Good morning, good afternoon, good evening everyone wherever you are.

Total users of this bot have reached 77k 🎉🎉

Hopefully this bot will continue to be active, even though the response is very long hahaha

my YouTube channel total subscribers reached 1,970, please help me to reach 2,000 subscribers.

my youtube channel: https://youtube.com/@fawwazthoerif

You can also donate to the bot maintenance process via the link below: 

Trakteer (Indonesia): https://trakteer.id/fawwazthoerif
Sociabuzz (International): https://sociabuzz.com/fawwazthoerif/tribe

Thank you

Greetings, @AkasakaID
'''

listUser = requests.get("https://api.akasakaid.dev/api/getusertiktok").json()
for user in listUser:
    print('~' * 50)
    userId = user["user_id"]
    sendMessage(chat_id=userId,message=textMessage,message_id=None)
    print('- success send message to userid :',userId)