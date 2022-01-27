import os
import re
import sys
import json
import requests
from bs4 import BeautifulSoup as bs

class Tiktok:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66"}
    
    def savetiktok(self,url):
        try:
            print("~> SAVETIKTOK <~")
            r = requests.Session()
            req = r.get("https://savetiktok.cc/en/download?url=" + url ,headers=self.headers)
            if "Extract the TikTok video link failed" in req.text:
                print("~> video private / removed <~")
                print("~> failed download <~")
                return "private/removed"
            videoid = re.search('video_id=(.*?)&',req.text).group(1)
            url = f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/play/?video_id={videoid}&line=0&is_play_url=1&source=PackSourceEnum_AWEME_DETAIL'
            self.save(url=url)
            return True
        except AttributeError:
            print("~> failed download <~")
            return False
    
    def musicallydown(self,url):
        try:
            print("~> MUSICALLYDOWN <~")
            r = requests.Session()
            req = r.get("https://musicaldown.com/",headers=self.headers)
            AllName = re.findall('input name="(.*?)"',req.text)
            AllValue = re.findall('value="(.*?)"',req.text)
            data = {AllName[0]:url,AllName[1]:AllValue[0],AllName[2]:AllValue[1]}
            req = r.post(f"https://musicaldown.com/download",data=data,headers=self.headers)
            if "Video is private or removed!" in req.text:
                print("~> video private/removed <~")
                return "private/removed"
            parsing = bs(req.text,'html.parser')
            links = parsing.findAll("a",attrs={"target":"_blank"})
            if len(links) == 3:
                self.save(url=links[2]["href"])
                return True
            elif len(links) == 2:
                self.save(url=links[1]["href"])
                return True
            elif len(links) == 1:
                self.save(url=links[0]["href"])
                return True
        except AttributeError:
            print("~> failed download <~")
            return False

    def save(self,url):
        content = requests.get(url).content
        open("video.mp4","wb").write(content)
        print("~> DOWNLOAD SUCCESS <~")
