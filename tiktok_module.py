import os
import re
import sys
import json
import requests
from bs4 import BeautifulSoup as bs

class Tiktok:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66"}
    
    def musicallydown(self,url:str = None):
        try:
            r = requests.Session()
            req = r.get("https://musicaldown.com/",headers=self.headers)
            AllName = re.findall('input name="(.*?)"',req.text)
            AllValue = re.findall('value="(.*?)"',req.text)
            data = {
                AllName[0]:url,
                AllName[1]:AllValue[0],
                AllName[2]:AllValue[1]
                }
            req = r.post(f"https://musicaldown.com/download",data=data,headers=self.headers)
            if "Video is private or removed!" in req.text:
                print("~> video private/removed <~")
                return "private/removed"
            res = re.findall(
                '<a style="margin-top:10px;" target="_blank" rel="noreferrer" href="(.*?)"',req.text
            )
            if len(res) == 0:return False
            self.save(res[0])
            
        except AttributeError:
            print("~> download failure <~")
            return False

    def save(self,url):
        content = requests.get(url).content
        open("video.mp4","wb").write(content)
        print("~> download successed <~")
