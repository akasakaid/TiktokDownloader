# Tiktok Downloader

This is a repository for telegram bot tiktok downloader without watermark [https://t.me/TiktokVideoDownloaderIDBot](https://t.me/TiktokVideoDownloaderIDBot)

but you can also use the module I have created 
```
# python
>> from tiktok_module import downloader
>>
>> dl = downloader.tiktok_downloader()
>> result = dl.musicaldown(url="https://tiktok.com/...",output_name="video.mp4")
>>
```

### How to run in local machine :
 1. Create you own bot on [BotFather](https://t.me/BotFather)
 2. Download or clone repository
 3. Open folder repository
 4. copy .env.example to .env
 5. paste token bot to variable token_bot like example on it
 6. Install module on requirements.txt
```
python3 -m pip install -r requirements.txt
```
 6. Run file bot_polling.py
```
python3 bot_polling.py
```