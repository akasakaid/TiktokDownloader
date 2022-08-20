# Tiktok Downloader

This is a repository for telegram bot tiktok downloader without watermark [TiktokVideoDownloaderIDBot](https://t.me/TiktokVideoDownloaderIDBot)

but you can also use the module I have created 
```
# python
>> from tiktok_module import downloader
>>
>> dl = downloader.tiktok_downloader()
>> result = dl.musicaldown(url="https://tiktok.com/...",output_name="video.mp4")
>>
```

## How to run in local machine :
 1. Create you own bot on [BotFather](https://t.me/BotFather)
 2. Download or clone repository
 3. Open folder repository
 4. edit config.py, paste your token
 5. Install module on requirements.txt<br>
`python3 -m pip install -r requirements.txt`
 6. Run file bot_polling.py<br>
`python3 bot_polling.py`