import utils
import pathlib
import pyrogram
import databases
import tiktok_downloader
from load import *
from models import users, videos
from datetime import datetime, timezone

cwd = pathlib.Path(__file__).parent

bot = pyrogram.Client(
    name="tiktok-bot", api_id=api_id, api_hash=api_hash, bot_token=token_bot
)


async def start_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    first_name = message.chat.first_name
    username = message.chat.username
    last_name = message.chat.last_name
    userid = message.chat.id
    text = message.text
    print(f"{userid} {first_name} - {text}")
    query = "SELECT * FROM users WHERE user_id = :userid"
    values = {"userid": userid}
    async with databases.Database(DATABASE) as database:
        result = await database.fetch_one(query=query, values=values)
        if result is None:
            query = users.insert()
            values = {
                "user_id": userid,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "created_at": datetime.now(tz=timezone.utc)
                .now()
                .isoformat()
                .split(".")[0],
            }
            await database.execute(query=query, values=values)
    msgid = message.id
    retext = f"""Welcome {first_name} to Tiktok Video Downloader Bot

How to use :

ID : Cara menggunakan bot hanya dengan mengirimkan tautan dari video tiktok yang ingin kamu unduh.

EN : How to use the bot by simply sending the link of the tiktok video you want to download.
    """
    await client.send_message(chat_id=userid, text=retext, reply_to_message_id=msgid)
    return


async def tiktok_handler(client: pyrogram.Client, message: pyrogram.types.Message):
    userid = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    username = message.chat.username
    text = message.text
    msgid = message.id
    print(f"{userid} {first_name} - {text}")
    query = "SELECT * FROM users WHERE user_id = :userid"
    values = {"userid": userid}
    async with databases.Database(DATABASE) as database:
        result = await database.fetch_one(query=query, values=values)
        if result is None:
            query = users.insert()
            values = {
                "user_id": userid,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "created_at": datetime.now(tz=timezone.utc)
                .now()
                .isoformat()
                .split(".")[0],
            }
            await database.execute(query=query, values=values)
    video_id, author_id, author_username = await utils.get_video_detail(text)
    if video_id is None:
        retext = "The tiktok video you want to download doesn't exist, it might be deleted or a private video."
        await client.send_message(
            chat_id=userid, text=retext, reply_to_message_id=msgid
        )
        return
    link_length = len(text)
    source_link = f"[Video Source]({text})"
    retext = f"""Successfully download the video 

{(source_link if link_length > 40 else '')}

Powered by @TiktokVideoDownloaderIDBot"""
    keylist = [
        [
            pyrogram.types.InlineKeyboardButton(text="Source Video", url=text),
        ],
        [
            pyrogram.types.InlineKeyboardButton(
                text="Follow Me", url="https://t.me/fawwazthoerif"
            ),
            pyrogram.types.InlineKeyboardButton(
                text="Donation", callback_data="donation"
            ),
        ],
    ]
    if link_length > 40:
        keylist.pop(0)
    rekey = pyrogram.types.InlineKeyboardMarkup(inline_keyboard=keylist)
    async with databases.Database(DATABASE) as database:
        query = "SELECT * FROM videos WHERE video_id = :video_id AND author_id = :author_id OR author_username = :author_username"
        values = {
            "video_id": video_id,
            "author_id": author_id,
            "author_username": author_username,
        }
        result = await database.fetch_one(query=query, values=values)
        if result is not None:
            file_id = result.file_id
            file_unique_id = result.file_unique_id
            await client.delete_messages(chat_id=userid, message_ids=msgid)
            await client.send_cached_media(
                chat_id=userid, file_id=file_id, caption=retext, reply_markup=rekey
            )
            return
    now = int(datetime.now(tz=timezone.utc).timestamp())
    output = cwd.joinpath(f"{now}.mp4")
    result = await tiktok_downloader.musicaldown(url=text, output=output)
    await client.delete_messages(chat_id=userid, message_ids=msgid)
    result = await client.send_video(
        chat_id=userid, video=output, caption=retext, reply_markup=rekey
    )
    file_id = result.video.file_id
    file_unique_id = result.video.file_unique_id
    async with databases.Database(DATABASE) as database:
        query = videos.insert()
        values = {
            "author_id": author_id,
            "author_username": author_username,
            "video_id": video_id,
            "file_id": file_id,
            "file_unique_id": file_unique_id,
            "created_at": datetime.now(tz=timezone.utc).now().isoformat().split(".")[0],
        }
        await database.execute(query=query, values=values)
    output.unlink(missing_ok=True)
    return


async def donation_handler(
    client: pyrogram.Client,
    message: pyrogram.types.Message | pyrogram.types.CallbackQuery,
):
    if isinstance(message, pyrogram.types.Message):
        userid = message.chat.id
        first_name = message.chat.first_name
        text = message.text
    if isinstance(message, pyrogram.types.CallbackQuery):
        userid = message.from_user.id
        first_name = message.from_user.first_name
        text = message.data
    print(f"{userid} {first_name} - {text}")
    retext = """If you like my work, you can support me through the link below.
    
International : https://sociabuzz.com/fawwazthoerif/tribe
Indonesia : https://trakteer.id/fawwazthoerif/tip

CRYPTO
USDT (TON) : `UQDicJd7KwBcxzqbn6agUc_KVl8BklzyvuKGxEVG7xuhnTFt`
    """
    await client.send_message(
        chat_id=userid, text=retext, disable_web_page_preview=True
    )
    return


async def main():
    print(f"start bot !")
    await bot.start()
    me = await bot.get_me()
    botname = me.first_name
    botuname = me.username
    print(f"Bot name : {botname}")
    print(f"Bot username : {botuname}")
    bot.add_handler(
        handler=pyrogram.handlers.message_handler.MessageHandler(
            callback=start_handler,
            filters=pyrogram.filters.command(commands=["start"]),
        )
    )
    bot.add_handler(
        handler=pyrogram.handlers.message_handler.MessageHandler(
            callback=tiktok_handler,
            filters=pyrogram.filters.regex(r"tiktok"),
        )
    )
    bot.add_handler(
        handler=pyrogram.handlers.message_handler.MessageHandler(
            callback=donation_handler,
            filters=pyrogram.filters.regex(r"donation"),
        )
    )
    bot.add_handler(
        handler=pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            callback=donation_handler,
            filters=pyrogram.filters.regex(r"donation"),
        )
    )
    await pyrogram.idle()
    await bot.stop()


import asyncio

bot.run(main())
