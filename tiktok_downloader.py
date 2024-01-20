import re
import random
import requests
from bs4 import BeautifulSoup as bs
from helper import random_ua, get_content

class downloader:
	def __init__(self,output_name:str):
		self.output_name = output_name

	def tiktapio(self,url:str):
		ses = requests.Session()
		ses.headers.update({
			'Accept': 'application/json',
			'Accept-Language': 'en-US,en;q=0.9',
			'Content-Length': '53',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Cookie': 'pll_language=en; PHPREFS=full',
			'Origin': 'https://tiktap.io',
			'Referer': 'https://tiktap.io/',
			'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
			'Sec-Ch-Ua-Mobile': '?0',
			'Sec-Ch-Ua-Platform': '"Windows"',
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			"User-Agent": random_ua()
		})

		data = {
			"url": url,
			"token": ""
		}
		ses.headers.update({
			"Content-Length": str(len(str(data)))
		})
		res = ses.post("https://tiktap.io/api.php",data=data)
		if res.json()["status"] != "success":
			return False

		videoData = res.json()["video_data"]

		if "nwm_video_url_HQ" in videoData.keys():
			video_url = res.json()["video_data"]["nwm_video_url_HQ"]
			res = get_content(video_url, self.output_name)
			return res

		if "nwm_video_url" in videoData.keys():
			video_url = res.json()["video_data"]["nwm_video_url"]
			res = get_content(video_url, self.output_name)
			return res
		
		return False
	
	def snaptikpro(self,url:str):
		try:
			ses = requests.Session()
			ses.headers.update({
				"User-Agent": random_ua()
			})

			res = ses.get("https://snaptik.pro/")
			token = re.search('<input type="hidden" name="token" value="(.*?)">',res.text).group(1)
			data = {
				"url": url,
				"token": token,
				"submit": "1"
			}
			res = ses.post("https://snaptik.pro/action",data=data)

			if res.json()["error"]:
				return False

			video_url = re.search('<div class="btn-container mb-1"><a href="(.*?)" target="_blank" rel="noreferrer">',res.json()["html"]).group(1)
			if len(video_url) <= 0:
				return False

			res = get_content(video_url, self.output_name)
			return res
		
		except AttributeError:
			return False
		
	def tiktapiocom(self,url:str):
		try:
			ses = requests.Session()
			ses.headers.update({
				'User-Agent': random_ua()
			})
			res = ses.get('https://tiktokio.com/id/')
			open('hasil.html','w',encoding='utf-8').write(res.text)
			prefix = re.search(r'<input type="hidden" name="prefix" value="(.*?)"/>',res.text).group(1)
			data = {
				'prefix': prefix,
				'vid': url
			}
			ses.headers.update({
				'Content-Length': str(len(str(data))),
				'Content-Type': 'application/x-www-form-urlencoded',
				'Hx-Current-Url': 'https://tiktokio.com/',
				'Hx-Request': 'true',
				'Hx-Target': 'tiktok-parse-result',
				'Hx-Trigger': 'search-btn'
			})
			res = ses.post('https://tiktokio.com/api/v1/tk-htmx',data=data)
			parser = bs(res.text,'html.parser')
			video_url = parser.find_all('div',attrs={'class': 'tk-down-link'})[0].find('a').get('href')
			res = get_content(video_url, self.output_name)
			return res
		
		except KeyError:
			return False
		except AttributeError:
			return False
		except IndexError:
			return False
	
	def tikmatecc(self,url:str):
		try:
			headers = {
				"Host": "tikmate.cc",
				"accept": "application/json, text/javascript, */*; q=0.01",
				"user-agent": "Mozilla/5.0 (Linux; Android 11; CPH2061 Build/RKQ1.200903.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
				"origin": "https://ttmate.io",
				"x-requested-with": "mark.via.gp",
				"sec-fetch-site": "cross-site",
				"sec-fetch-mode": "cors",
				"sec-fetch-dest": "empty",
				"referer":"https://ttmate.io/",
				"accept-language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7,tr-TR;q=0.6,tr;q=0.5"
			}
			api = "https://tikmate.cc/analyze"
			params = {
				"url": url,
				"site": "tiktok"
			}
			res = requests.get(api,params=params,headers=headers)
			if res.text[0] != "{":
				return False
	
			error = res.json()["error"]
			if error:
				return False
	
			videoUrl = res.json()["formats"]["video"][0]["url"]
			res = get_content(videoUrl, self.output_name)
			return res
	
		except AttributeError:
			return False
	
		except IndexError:
			return False
	
		except KeyError:
			return False
	
	def musicaldown(self,url:str):
		ses = requests.Session()
		ses.headers.update({
			"User-Agent": random_ua()
		})
		res = ses.get("https://musicaldown.com/en")
		open("hasil.html","w",encoding="utf-8").write(res.text)
		parsing = bs(res.text,'html.parser')
		allInput = parsing.findAll('input')
		data = {}
		for i in allInput:
			if i.get("id") == "link_url":
				data[i.get("name")] = url
				continue

			data[i.get("name")] = i.get("value")

		res = ses.post("https://musicaldown.com/download",data=data,allow_redirects=True)
		if res.text.find("Convert Video Now") >= 0:
			data = re.search(r"data: '(.*?)'",res.text).group(1)
			urlSlider = re.search(r"url: '(.*?)'",res.text).group(1)
			res = ses.post(urlSlider,data={"data": data})
			if res.text.find('"success":true') >= 0:
				urlVideo = res.json()["url"]
				res = get_content(urlVideo, self.output_name)
				return res

			return False

		parsing = bs(res.text,'html.parser')
		allUrlDownload = parsing.findAll("a",attrs={"style":"margin-top:10px;"})
		if len(allUrlDownload) <= 0:
			return False

		i = random.randint(0,1)
		urlVideo = allUrlDownload[i].get("href")
		res = get_content(urlVideo, self.output_name)
		return res
