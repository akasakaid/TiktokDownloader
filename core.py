import json
from requests import *
from tiktok_downloader import downloader
from datetime import datetime
from telegram import send_message, send_video, delete_message


def get_time(tt):
    tt = datetime.fromtimestamp(tt)
    hour = str(tt.hour).zfill(2)
    minute = str(tt.minute).zfill(2)
    second = str(tt.second).zfill(2)
    day = str(tt.day).zfill(2)
    mon = str(tt.month).zfill(2)
    year = str(tt.year).zfill(4)

    return f"{year}-{mon}-{day} {hour}:{minute}:{second}"


def Core(data):
    try:
        video_name = "video.mp4"
        dl = downloader(video_name)
        user_id = None
        first_name = None
        text = None
        chat_type = data["message"]["chat"]["type"]
        message_date = data["message"]["date"]
        message_id = data["message"]["message_id"]

        if "first_name" in data["message"]["chat"].keys():
            first_name = data["message"]["chat"]["first_name"]

        if "id" in data["message"]["chat"].keys():
            user_id = data["message"]["chat"]["id"]

        if "text" in data["message"].keys():
            text = data["message"]["text"]

        if chat_type != "private":
            send_message(
                user_id, "Bot only work in private chat not group chat !", message_id
            )
            return

        rl_time = get_time(message_date)
        print(f"[+] time : {rl_time}")
        print(f"[+] from : {user_id} | {first_name}")
        print(f"[+] message : {text}")
        if text.startswith("/start"):
            msg = """Welcome to Tiktok Video Downloader Bot !

How to use the bot :
🇺🇸 : just send tiktok video link

Cara menggunakan bot :
🇮🇩 : cukup kirimkan tautan/url video tiktok

check video : https://vt.tiktok.com/ZSNLApQoG/"""
            send_message(user_id, msg, message_id)
            return

        if (
            "https://" in text
            and "tiktok.com" in text
            and len(text.split()) == 1
            and text.find("http") == 0
        ):
            original_link = text.split("?")[0] if text.find("?") >= 0 else text
            msg = f"""Video Downloaded from @TiktokVideoDownloaderIDBot!

🇺🇸 : if the video does not play, resend the link !
🇮🇩 : jika video tidak bisa diputar, kirim ulang url !

original link : {original_link}

Subscribe : https://youtube.com/@fawwazthoerif
Follow : https://tiktok.com/@fawwaz.thoerif

Donation :
🇺🇸 : https://sociabuzz.com/fawwazthoerif/tribe
🇮🇩 : https://trakteer.id/fawwazthoerif/tip"""

            res = dl.tiktapio(text)
            if res:
                print("[+] success download with tiktapio !")
                delete_message(user_id, message_id)
                send_video(user_id, video_name, msg)
                return

            res = dl.tiktapiocom(text)
            if res:
                print("[+] success download with tiktapiocom !")
                delete_message(user_id, message_id)
                send_video(user_id, video_name, msg)
                return

            res = dl.tikmatecc(text)
            if res:
                print("[+] success download with tikmatecc !")
                delete_message(user_id, message_id)
                send_video(user_id, video_name, msg)
                return

            res = dl.snaptikpro(text)
            if res:
                print("[+] success download with snaptikpro !")
                delete_message(user_id, message_id)
                send_video(user_id, video_name, msg)
                return

            res = dl.musicaldown(text)
            if res:
                print("[+] success download with musicaldown !")
                delete_message(user_id, message_id)
                send_video(user_id, video_name, msg)
                return

            msg = """🇺🇸 : failed to download the video, check the link and try again later !
🇮🇩 : gagal dalam mengunduh video, cek tautan dan coba lagi nanti !"""
            send_message(user_id, msg, message_id)
            return

        if text.startswith("/donation"):
            msg = """Support my project by donating as much as you can for server and maintenance costs.

Indonesia : https://trakteer.id/fawwazthoerif/tip
Global (International) : https://sociabuzz.com/fawwazthoerif/tribe"""
            send_message(user_id, msg, message_id)
            return

    except Exception as e:
        print(f"[x] {e}")
        open(".log", "a+", encoding="utf-8").write(str(data) + "\n")
        return
